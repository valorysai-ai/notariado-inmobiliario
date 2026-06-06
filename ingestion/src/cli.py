import typer
from loguru import logger
from ingestion.src.pipeline import run_pipeline, LAYERS

app = typer.Typer()


@app.command()
def run(
    layers: list[str] = typer.Option(
        default=LAYERS,
        help="Layers to ingest. Options: nacional, ccaa, provincia, municipio, codigo_postal",
    )
):
    logger.info(f"Running pipeline for layers: {layers}")
    run_pipeline(layers)


if __name__ == "__main__":
    app()