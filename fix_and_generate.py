from pathlib import Path

source = Path("generate_sih_pdf.py").read_text(encoding="utf-8")
source = source.replace(
    'name="Code", parent=styles["Code"]',
    'name="CodeCustom", parent=styles["Code"]',
)
source = source.replace('styles["Code"]))', 'styles["CodeCustom"]))')
exec(compile(source, "generate_sih_pdf.py", "exec"), {"__name__": "__main__"})
