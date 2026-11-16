#!/bin/bash
# Local audit helper. Git and Python read tracked files; tee writes audit_bundle.txt.
set -euo pipefail

audit_script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
audit_repo_root="$(git -C "$audit_script_dir/.." rev-parse --show-toplevel)"
cd "$audit_repo_root"
export GIT_OPTIONAL_LOCKS=0
if ! git check-ignore -q -- audit_bundle.txt; then
    printf 'AUDIT ERROR: audit_bundle.txt must be ignored locally before running this helper.\n' >&2
    exit 1
fi

{
    printf 'LineGuide local repository audit\n'
    printf 'UTC time: %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    printf 'Repository: %s\n' "$audit_repo_root"
    printf 'Scope: tracked working-tree files; Git HEAD tree is listed separately.\n'
    printf 'Output: ignored local audit_bundle.txt. This helper performs no commit or push.\n'
    printf 'Discovery excludes untracked files and .git contents.\n'
    printf 'This extraction covers XML text, table cells and speaker notes. Images require visual review; no OCR is performed.\n'

    printf '\n=== 1. GIT BRANCH, REMOTE & COMMIT STATE ===\n'
    git --no-pager status -sb
    git remote -v
    git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null || printf 'origin/HEAD not set locally\n'
    git --no-pager branch -vv
    git --no-pager log -n 5 --oneline --decorate

    printf '\n=== 2. HEAD TREE & GIT BLOB BYTE SIZES ===\n'
    git --no-pager ls-tree -r --long HEAD

    PYTHONIOENCODING=utf-8 python3 - <<'PY'
import hashlib
import json
import os
from pathlib import Path
import posixpath
import subprocess
import sys
from urllib.parse import unquote
import zipfile
import xml.etree.ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}
LFS_PREFIX = b"version https://git-lfs.github.com/spec/v1"
repo_root = Path.cwd().resolve()


def label(value):
    return json.dumps(str(value), ensure_ascii=False)


def tracked_paths():
    raw = subprocess.check_output(["git", "ls-files", "-z"])
    return sorted(set(os.fsdecode(name) for name in raw.split(b"\0") if name))


def selected(name):
    path = Path(name)
    return path.name.upper().startswith("README") or path.suffix.lower() in {
        ".md", ".pdf", ".pptx"
    }


def read_tracked(name):
    path = repo_root / name
    if path.is_symlink():
        raise ValueError("selected tracked file is a symlink: " + label(name))
    try:
        path.resolve().relative_to(repo_root)
    except ValueError:
        raise ValueError("selected tracked file resolves outside the repository: " + label(name))
    if not path.is_file():
        raise ValueError("selected tracked file is missing or is not a regular file: " + label(name))
    data = path.read_bytes()
    if data.startswith(LFS_PREFIX):
        raise ValueError("Git LFS pointer found in working tree; fetch the real file before auditing: " + label(name))
    return data


def xml_part(archive, name):
    try:
        return ET.fromstring(archive.read(name))
    except KeyError:
        raise ValueError("missing OOXML part: " + label(name))
    except ET.ParseError as exc:
        raise ValueError("invalid XML in " + label(name) + ": " + str(exc))


def relationships(archive, source_part, required=False):
    rels_part = posixpath.join(
        posixpath.dirname(source_part), "_rels", posixpath.basename(source_part) + ".rels"
    )
    if rels_part not in archive.namelist():
        if required:
            raise ValueError("missing relationship part: " + label(rels_part))
        return {}
    root = xml_part(archive, rels_part)
    rels = {}
    for rel in root.findall("pr:Relationship", NS):
        rel_id = rel.get("Id")
        if not rel_id or rel_id in rels:
            raise ValueError("missing or duplicate relationship ID in " + label(rels_part))
        rels[rel_id] = rel
    return rels


def resolve_target(source_part, relationship):
    if relationship.get("TargetMode", "Internal").lower() == "external":
        raise ValueError("external slide or notes relationship in " + label(source_part))
    target = relationship.get("Target")
    if not target:
        raise ValueError("empty relationship target in " + label(source_part))
    target = unquote(target)
    if "\\" in target or "?" in target or "#" in target:
        raise ValueError("unsupported OOXML part target: " + label(target))
    if target.startswith("/"):
        part = posixpath.normpath(target.lstrip("/"))
    else:
        part = posixpath.normpath(posixpath.join(posixpath.dirname(source_part), target))
    if part in {".", ".."} or part.startswith("../"):
        raise ValueError("OOXML part target escapes archive root: " + label(target))
    return part


def paragraph_text(paragraph):
    # Descendant a:t includes regular runs, field runs and text in table cells.
    chunks = []
    for node in paragraph.iter():
        if node.tag == "{" + NS["a"] + "}t":
            chunks.append(node.text or "")
        elif node.tag == "{" + NS["a"] + "}br":
            chunks.append("\n")
        elif node.tag == "{" + NS["a"] + "}tab":
            chunks.append("\t")
    return "".join(chunks).strip()


def text_lines(root, skip_slide_number=False):
    skipped_paragraphs = set()
    if skip_slide_number:
        for shape in root.findall(".//p:sp", NS):
            placeholder = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
            if placeholder is not None and placeholder.get("type") == "sldNum":
                skipped_paragraphs.update(shape.findall(".//a:p", NS))
    return [
        text for paragraph in root.findall(".//a:p", NS)
        if paragraph not in skipped_paragraphs
        for text in [paragraph_text(paragraph)] if text
    ]


def extract_deck(name, data):
    import io
    print("\n[DECK: " + label(name) + "]")
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            bad_member = archive.testzip()
            if bad_member is not None:
                raise ValueError("ZIP integrity check failed at " + label(bad_member))
            presentation_part = "ppt/presentation.xml"
            presentation = xml_part(archive, presentation_part)
            rels = relationships(archive, presentation_part, required=True)
            slide_ids = presentation.findall("p:sldIdLst/p:sldId", NS)
            if not slide_ids:
                raise ValueError("presentation has no slides in its display-order list")
            notes_parts = 0
            notes_with_text = 0
            paragraphs = 0
            table_cells = 0
            for display_index, slide_id in enumerate(slide_ids, 1):
                rel_id = slide_id.get("{" + NS["r"] + "}id")
                if rel_id not in rels:
                    raise ValueError("missing slide relationship " + label(rel_id))
                slide_rel = rels[rel_id]
                if not slide_rel.get("Type", "").endswith("/slide"):
                    raise ValueError("display-order relationship is not a slide: " + label(rel_id))
                slide_part = resolve_target(presentation_part, slide_rel)
                slide = xml_part(archive, slide_part)
                lines = text_lines(slide)
                cells = slide.findall(".//a:tc", NS)
                table_cells += len(cells)
                paragraphs += len(lines)
                print("\n--- Slide " + str(display_index) + " (part: " + slide_part + ") ---")
                print("[Table cells: " + str(len(cells)) + "]")
                if lines:
                    for line in lines:
                        print("  " + line.replace("\n", "\n  "))
                else:
                    print("  [No extractable slide text]")

                note_rels = [
                    rel for rel in relationships(archive, slide_part).values()
                    if rel.get("Type", "").endswith("/notesSlide")
                ]
                if len(note_rels) > 1:
                    raise ValueError("multiple notes-slide relationships in " + label(slide_part))
                if not note_rels:
                    print("  [Speaker Notes]: no notes relationship")
                    continue
                notes_part = resolve_target(slide_part, note_rels[0])
                notes_root = xml_part(archive, notes_part)
                notes_parts += 1
                note_lines = text_lines(notes_root, skip_slide_number=True)
                print("  [Speaker Notes part: " + notes_part + "]")
                if note_lines:
                    notes_with_text += 1
                    print("  [Speaker Notes]:")
                    for line in note_lines:
                        print("    " + line.replace("\n", "\n    "))
                else:
                    print("  [Speaker Notes]: no extractable text after excluding slide-number placeholders")
            print(
                "\nDECK SUMMARY: path=" + label(name)
                + " slides=" + str(len(slide_ids))
                + " notes_parts=" + str(notes_parts)
                + " notes_with_text=" + str(notes_with_text)
                + " slide_text_paragraphs=" + str(paragraphs)
                + " table_cells=" + str(table_cells)
            )
            return len(slide_ids), notes_parts, notes_with_text
    except (zipfile.BadZipFile, zipfile.LargeZipFile, RuntimeError, ValueError) as exc:
        raise ValueError("deck " + label(name) + ": " + str(exc))


def main():
    names = [name for name in tracked_paths() if selected(name)]
    files = {}
    print("\n=== 3. SHA-256, WORKING-TREE BYTE SIZES & LFS POINTER CHECK ===")
    print("Columns: SHA-256 | bytes | LFS pointer prefix | tracked path")
    for name in names:
        data = read_tracked(name)
        files[name] = data
        print(hashlib.sha256(data).hexdigest() + " | " + str(len(data)) + " | absent | " + label(name))
    print("HASH SUMMARY: files=" + str(len(files)) + " lfs_pointers=0")

    print("\n=== 4. TRACKED README CONTENT ===")
    readmes = [name for name in names if Path(name).name.upper().startswith("README")]
    if not readmes:
        print("[No tracked README files]")
    for name in readmes:
        print("\n--- " + label(name) + " ---")
        print(files[name].decode("utf-8", errors="replace"))
    print("README SUMMARY: files=" + str(len(readmes)))

    print("\n=== 5. PPTX SLIDE, TABLE-CELL & SPEAKER-NOTES EXTRACTION ===")
    decks = [name for name in names if Path(name).suffix.lower() == ".pptx"]
    totals = [0, 0, 0]
    if not decks:
        print("[No tracked PPTX files]")
    for name in decks:
        counts = extract_deck(name, files[name])
        totals = [previous + current for previous, current in zip(totals, counts)]
    print(
        "\nEXTRACTION SUMMARY: decks=" + str(len(decks))
        + " slides=" + str(totals[0])
        + " notes_parts=" + str(totals[1])
        + " notes_with_text=" + str(totals[2])
    )
    print("AUDIT RESULT: completed")


try:
    main()
except (OSError, subprocess.CalledProcessError, ValueError, ET.ParseError) as exc:
    print("\nAUDIT ERROR: " + str(exc), flush=True)
    sys.exit(1)
PY
} 2>&1 | tee "$audit_repo_root/audit_bundle.txt"
