"""Build static HTML site from directory of HTML templates and plain files."""
import pathlib
import click
import jinja2
import json

@click.command(help="Templated static website generator.")
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
    def copy_static(src: pathlib.Path, dst: pathlib.Path):
        dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            target = dst / item.name
            if item.is_dir():
                # Recursive call for subdirectory
                copy_static(item, target)
            else:
                # Copy file contents
                target.write_bytes(item.read_bytes())

    input_dir = pathlib.Path(input_dir)
    # print(f"DEBUG input_dir={input_dir}")
    output_dir = pathlib.Path("generated_html")
    if output:
        # print(f"DEBUG output_dir={output}")
        # output = output.lstrip("/")  # remove leading slash
        output_dir = pathlib.Path(output)  # convert str to Path object, when --output is provided
        # output_path = output_dir/output/"index.html"
    if output_dir.exists():
        click.echo(f"insta485generator error: {output_dir} already exists", err=True)
        exit(1)

    config_filename = input_dir / "config.json"
    with config_filename.open() as config_file:
        # config_filename is open within this code block
        config_list = json.load(config_file)
        # print(json.dumps(config_list, indent=2))
    # config_filename is automatically closed

    # template_filename = input_dir / "templates/index.html"
    # with template_filename.open() as template_file:
    #     # config_filename is open within this code block
    #     template_list = template_file.read()
    #     # print(template_list)

    
    template_dir = pathlib.Path(input_dir / "templates")

    template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(template_dir)),
    autoescape=jinja2.select_autoescape(['html', 'xml']),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    for entry in config_list:
        url = entry["url"]
        template_name = entry["template"]
        context = entry["context"]
        template = template_env.get_template(template_name)

        # if url == "/":
        #     logname = context.get("logname")

        #     # Find the following page for this user
        #     following_page = next(
        #         (p for p in config_list
        #         if p["url"] == f"/users/{logname}/following/"), None
        #     )
        #     if "posts" in context:
        #         if following_page is not None:

        #             following_users = [
        #                 f["username"] for f in following_page["context"]["following"]
        #             ]

        #             # Keep only posts by followed users (or self)
        #             context["posts"] = [
        #                 p for p in context["posts"]
        #                 if p["owner"] in following_users or p["owner"] == logname
        #             ]
        #         else:
        #             context["posts"] = [
        #                 p for p in context["posts"]
        #                 if p["owner"] in following_users or p["owner"] == logname
        #             ]

        # Render template with context (variables for substitution)
        rendered_html = template.render(**context)

    # Write rendered HTML to file
        url = url.lstrip("/")
        output_path = output_dir / url / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            f.write(rendered_html)

        if verbose:
            print(f"Rendered {template_name} -> {output_path}")

    ## Checking for static dir
    static_dir = input_dir / "static"
    if static_dir.exists() and static_dir.is_dir():
        copy_static(static_dir, output_dir)
        if verbose:
            print(f"Copied {static_dir} -> {output_dir}")





if __name__ == "__main__":
    main()
