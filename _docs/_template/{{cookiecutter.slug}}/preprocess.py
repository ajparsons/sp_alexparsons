try:
    from stringprint2.stringprint.tools.preprocessing import (
        BasePreprocess,
        SectionMove,
        SectionDelete,
        TextSnip,
    )
except ImportError:
    from stringprint.tools.preprocessing import (
        BasePreprocess,
        SectionMove,
        SectionDelete,
        TextSnip,
    )


class Preprocess(BasePreprocess):
    google_download: bool = True
    google_download_formats: list = ["contents.pdf", "doc_source.docx"]
    output_filename: str = "document.md"
    word_convert: bool = True
    word_source_file: str = "doc_source.docx"
    pdf_cover: str = "cover.pdf"
    pdf_contents: str = "contents.pdf"
    merge_pdfs: bool = True

    # list of callables that accept and return the text
    # of the document
    text_actions = [
        # SectionDelete("start")
        # SectionMove("# Header 1", after ="# Header 2")
    ]

    find_replace = [
        # ("old", "new")
    ]
