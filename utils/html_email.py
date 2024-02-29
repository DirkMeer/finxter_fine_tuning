import html2text


test_email = "paste example email from the dataset here"


def html_to_markdown(html: str) -> str:
    html = html.encode("utf-16", "surrogatepass").decode("utf-16")

    html_to_text_converter = html2text.HTML2Text()
    html_to_text_converter.ignore_links = False
    return html_to_text_converter.handle(html)


if __name__ == "__main__":
    markdown_content = html_to_markdown(test_email)

    with open("test.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)
