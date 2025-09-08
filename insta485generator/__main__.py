"""Build static HTML site from directory of HTML templates and plain files."""
import pathlib
import click
import jinja2
import json


@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option(
    "-o", "--output",
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    metavar="PATH",
    help="Output directory."
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Print more output."
)
def main(input_dir, output, verbose):
    input_dir = pathlib.Path(input_dir)
    print(f"DEBUG input_dir={input_dir}")
    if output:
        print(f"DEBUG output_dir={output}")
        output = output.lstrip("/")  # remove leading slash
        output_dir = pathlib.Path(output)  # convert str to Path object, when --output is provided
        output_path = output_dir/output/"index.html"

    if verbose:
        print("DEBUG verbose mode is ON")

    config_filename = input_dir / "config.json"
    with config_filename.open() as config_file:
        # config_filename is open within this code block
        config_list = json.load(config_file)
        print(json.dumps(config_list, indent=2))
    # config_filename is automatically closed

    template_filename = input_dir / "templates/index.html"
    with template_filename.open() as template_file:
        # config_filename is open within this code block
        template_list = template_file.read()
        print(template_list)

    template_dir = pathlib.Path("hello/templates")

    template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(template_dir)),
    autoescape=jinja2.select_autoescape(['html', 'xml']),
    )
    output_dir = pathlib.Path("generated_html")
    output_dir.mkdir(parents=True, exist_ok=True)
    for entry in config_list:
        url = entry["url"]
        template_name = entry["template"]
        context = entry["context"]
        template = template_env.get_template("index.html")

        # Render template with context (variables for substitution)
        rendered_html = template.render(**context)

    # Write rendered HTML to file
        output_path = output_dir / "index.html"
        with output_path.open("w", encoding="utf-8") as f:
            f.write(rendered_html)

    print(f"Wrote {output_path}")



if __name__ == "__main__":
    main()
