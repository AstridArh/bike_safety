"""Plotting helpers used by the regional network-overlap notebooks.

The former notebook defined plot_bicycle_networks twice. The active version
keeps its name; the optional-saving version is available as
plot_bicycle_networks_with_export.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

__all__ = [
    "plot_bicycle_networks",
    "plot_bicycle_networks_with_export",
    "plot_overlap_results",
    "plot_matched_attribute",
]


def plot_bicycle_networks_with_export(
    sample,
    bike_loops_edges,
    bike_loops_nodes,
    bike_loops_bbox_gdf,
    osm_edges,
    output_dir=None,
):
    """Plot the OSM extraction and BikeNodePlanner network."""
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="#fffffb")

    osm_edges.plot(
        ax=ax,
        color="#c8cdd2",
        linewidth=0.3,
        alpha=0.6,
        label="OSM bicycle network",
        zorder=1,
    )

    bike_loops_edges.plot(
        ax=ax,
        color="#16855b",
        linewidth=1.2,
        label="Bike loop network",
        zorder=2,
    )

    bike_loops_nodes.plot(
        ax=ax,
        color="#172b4d",
        markersize=3,
        label="Bike loop nodes",
        zorder=3,
    )

    bike_loops_bbox_gdf.boundary.plot(
        ax=ax,
        color="#d94841",
        linewidth=1,
        linestyle="--",
        label="Extraction boundary",
        zorder=4,
    )

    ax.set_title(f"{sample.title()} bicycle networks")

    # Use the extraction boundary as the plot extent
    minx, miny, maxx, maxy = (bike_loops_bbox_gdf.total_bounds)
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    ax.margins(0)
    ax.legend(loc="lower left")
    ax.set_axis_off()
    ax.set_aspect("equal")

    fig.tight_layout()

    # Save when an output directory is provided
    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        plot_path = (output_dir / f"{sample}_bicycle_networks.png")
        fig.savefig(plot_path, dpi=240, bbox_inches="tight")
        print("Saved plot:", plot_path)

    plt.show()
    return fig, ax


def plot_bicycle_networks(
    sample,
    bike_loops_edges,
    bike_loops_nodes,
    bike_loops_bbox_gdf,
    osm_edges,
):
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="#f7f7f5")

    osm_edges.plot(
        ax=ax,
        color="#c8cdd2",
        linewidth=0.3,
        alpha=0.6,
        label="OSM bicycle network",
        zorder=1,
    )

    bike_loops_edges.plot(
        ax=ax,
        color="#16855b",
        linewidth=1.2,
        label="Bike loop network",
        zorder=2,
    )

    bike_loops_nodes.plot(
        ax=ax,
        color="#172b4d",
        markersize=3,
        label="Bike loop nodes",
        zorder=3,
    )

    bike_loops_bbox_gdf.boundary.plot(
        ax=ax,
        color="#d94841",
        linewidth=1,
        linestyle="--",
        label="Extraction boundary",
        zorder=4,
    )

    # Use the extraction boundary as the plot extent
    minx, miny, maxx, maxy = (bike_loops_bbox_gdf.total_bounds)
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    ax.set_title(f"{sample.title()} bicycle networks")

    ax.legend(loc="lower left")
    ax.margins(0)
    ax.set_axis_off()
    ax.set_aspect("equal")

    fig.tight_layout(pad=0.2)
    plt.show()


def plot_overlap_results(
    sample,
    tolerance_m,
    output_dir,
    bike_loops_edges,
    bike_loops_nodes,
    osm_edges,
    bike_loops_overlap,
    matched_edges,
    unmatched_edges,
    plot_padding_m=0,
):
    """Calculate, print, plot and save network-overlap results."""
    total_length_m = bike_loops_overlap["bike_loop_length_m"].sum()
    matched_length_m = bike_loops_overlap["matched_length_m"].sum()
    unmatched_length_m = bike_loops_overlap["unmatched_length_m"].sum()

    coverage_pct = (
        100 * matched_length_m / total_length_m
        if total_length_m > 0
        else np.nan
    )

    print(f"Bike-loop length: {total_length_m / 1000:,.2f} km")
    print(f"Matched length: {matched_length_m / 1000:,.2f} km")
    print(f"Unmatched length: {unmatched_length_m / 1000:,.2f} km")
    print(f"Coverage: {coverage_pct:.2f}%")

    # Plot results
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="#f7f7f5")

    osm_edges.plot(
        ax=ax,
        color="#c8cdd2",
        linewidth=0.25,
        alpha=0.5,
        zorder=1,
    )

    matched_edges.plot(
        ax=ax,
        color="#16855b",
        linewidth=1.6,
        label="Matched",
        zorder=3,
    )

    if not unmatched_edges.empty:
        unmatched_edges.plot(
            ax=ax,
            color="#d94841",
            linewidth=2.3,
            label="Unmatched",
            zorder=4,
        )

    bike_loops_nodes.plot(
        ax=ax,
        color="#172b4d",
        markersize=4,
        label="Bike-loop nodes",
        zorder=5,
    )

    ax.set_title(f"{sample.title()} BikeNodePlanner–OSM overlap ({tolerance_m}m)\n {coverage_pct:.2f}% matched · {unmatched_length_m / 1000:.2f}km unmatched")

    # Set plot extent from the bike-loop network
    minx, miny, maxx, maxy = (bike_loops_edges.total_bounds)
    ax.set_xlim(minx - plot_padding_m, maxx + plot_padding_m)
    ax.set_ylim(miny - plot_padding_m, maxy + plot_padding_m)

    ax.margins(0)
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.legend(loc="lower left")
    fig.tight_layout(pad=0.1)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plot_path = output_dir / f"{sample}_overlap.png"
    fig.savefig(plot_path, dpi=240, bbox_inches="tight", pad_inches=0.05)
    plt.show()

    # Return results for later comparison
    return {
        "sample": sample,
        "tolerance_m": tolerance_m,
        "bike_loop_length_km": total_length_m / 1000,
        "matched_length_km": matched_length_m / 1000,
        "unmatched_length_km": unmatched_length_m / 1000,
        "coverage_pct": coverage_pct,
        "plot_path": plot_path,
    }


def plot_matched_attribute(
    sample,
    osm_edges,
    matched_edges,
    unmatched_edges,
    bike_loops_edges,
    bike_loops_nodes,
    tolerance_m,
    output_dir,
    plot_padding_m=1_000,
):
    lit_colors = {
        "missing": "#b8bcc2",
        "no": "#293241",
        "yes": "#f2b134",
    }

    surface_colors = {
        "missing": "#b8bcc2",
        "unpaved": "#b07d4f",
        "other": "#CC79A7",
        "paved": "#2a9d8f",
    }

    plot_settings = [
        {
            "attribute": "lit_group",
            "title": "Lighting (max coverage)",
            "colors": lit_colors,
        },
        {
            "attribute": "surface_group",
            "title": "Surface (max coverage)",
            "colors": surface_colors,
        },
    ]

    fig, axes = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(16, 8),
        facecolor="#fffffc",
    )

    minx, miny, maxx, maxy = (bike_loops_edges.total_bounds)

    for ax, settings in zip(axes, plot_settings):
        attribute = settings["attribute"]
        title = settings["title"]
        colors = settings["colors"]

        # OSM background
        osm_edges.plot(
            ax=ax,
            color="#e1e4e6",
            linewidth=0.2,
            alpha=0.5,
            zorder=1,
        )

        # Matched edges coloured by attribute
        for category, color in colors.items():
            category_edges = matched_edges.loc[matched_edges[attribute] == category]

            if not category_edges.empty:
                category_edges.plot(
                    ax=ax,
                    color=color,
                    linewidth=2,
                    label=category.title(),
                    zorder=3,
                )

        # Unmatched bike-loop geometry
        if not unmatched_edges.empty:
            unmatched_edges.plot(
                ax=ax,
                color="#d94841",
                linewidth=2.3,
                label="Unmatched",
                zorder=4,
            )

        # Bike-loop nodes
        bike_loops_nodes.plot(
            ax=ax,
            color="#172b4d",
            markersize=4,
            label="Bike-loop nodes",
            zorder=5,
        )

        ax.set_xlim(minx - plot_padding_m, maxx + plot_padding_m)
        ax.set_ylim(miny - plot_padding_m, maxy + plot_padding_m)

        ax.set_title(title, fontsize=14)
        ax.legend(loc="lower left", title=title, frameon=True)
        ax.margins(0)
        ax.set_axis_off()
        ax.set_aspect("equal")

    fig.suptitle(f"{sample.title()} matched bike-loop network ({tolerance_m} m OSM tolerance)", fontsize=16)

    fig.tight_layout(rect=[0, 0, 1, 0.95], pad=0.5)
    output_path = Path(output_dir) / f"{sample}_matched_lit_surface.png"
    fig.savefig(output_path, dpi=240, bbox_inches="tight", pad_inches=0.05)
    plt.show()
    print("Saved:", output_path)

    return fig, axes
