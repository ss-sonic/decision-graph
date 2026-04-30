from __future__ import annotations

import json
from pathlib import Path
from string import Template
from typing import Any

from .doc_artifacts import doc_artifact_schema
from .utils import read_text


DOC_ROLE_TO_TEMPLATE = {
    "extractor": "extractor.md",
    "researcher": "researcher.md",
    "improver": "improver.md",
    "skeptic": "skeptic.md",
    "editor": "editor.md",
    "judge": "judge.md",
}


def render_doc_prompt(
    root: Path,
    role: str,
    doc_path: Path,
    input_markdown: str,
    focus: str,
    context_sections: list[tuple[str, str]],
) -> str:
    template_path = root / "doc-prompts" / DOC_ROLE_TO_TEMPLATE[role]
    template = Template(read_text(template_path))
    rendered_context = "\n\n".join(
        f"## {title}\n{content}" for title, content in context_sections if content.strip()
    )
    return template.substitute(
        doc_path=str(doc_path),
        focus=focus,
        input_markdown=input_markdown,
        context_sections=rendered_context or "No prior artifacts available.",
        artifact_contract=json.dumps(doc_artifact_schema(role), indent=2),
    )
