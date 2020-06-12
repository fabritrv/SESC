// for reference see https://observablehq.com/@d3/circle-packing@164, this is a modified and stripped down version
export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["results_list.json", new URL("./files/search_results.json", import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], function (md) {
    return (
      md`# Your search results circle packed

Below you can find the results of your search: a contract contained in a bigger yellow circle will be a relevant result,
while smaller ones are less relevant. Hover the circles with the cursor to show the full address. The contracts contained inside the same light orange circle share the same level of relevance.
This visual representation was generated using a .json produced by SESC and D3’s [circle packing](https://observablehq.com/@d3/circle-packing).`
    )
  });
  main.variable(observer("chart")).define("chart", ["pack", "data", "d3", "width", "height", "DOM", "color", "format"], function (pack, data, d3, width, height, DOM, color, format) {
    const root = pack(data);

    const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height])
      .style("font", "10px sans-serif")
      .attr("text-anchor", "middle");

    const shadow = DOM.uid("shadow");

    svg.append("filter")
      .attr("id", shadow.id)
      .append("feDropShadow")
      .attr("flood-opacity", 0.3)
      .attr("dx", 0)
      .attr("dy", 1);

    const node = svg.selectAll("g")
      .data(d3.nest().key(d => d.height).entries(root.descendants()))
      .join("g")
      .attr("filter", shadow)
      .selectAll("g")
      .data(d => d.values)
      .join("g")
      .attr("transform", d => `translate(${d.x + 1},${d.y + 1})`);

    node.append("circle")
      .attr("r", d => d.r)
      .attr("fill", d => color(d.height));

    const leaf = node.filter(d => !d.children);

    leaf.select("circle")
      .attr("id", d => (d.leafUid = DOM.uid("leaf")).id);

    leaf.append("clipPath")
      .attr("id", d => (d.clipUid = DOM.uid("clip")).id)
      .append("use")
      .attr("xlink:href", d => d.leafUid.href);

    leaf.append("text")
      .attr("clip-path", d => d.clipUid)
      .selectAll("tspan")
      .data(d => d.data.name.split(/(?=[A-Z][a-z])|\s+/g))
      .join("tspan")
      .attr("x", 0)
      .attr("y", (d, i, nodes) => `${i - nodes.length / 2 + 0.8}em`)
      .text(d => d);

    node.append("title")
      .text(d => `${d.ancestors().map(d => d.data.name).reverse().join(" - ")}`);

    return svg.node();
  }
  );
  main.variable(observer("data")).define("data", ["FileAttachment"], function (FileAttachment) {
    return (
      FileAttachment("results_list.json").json()
    )
  });
  main.variable(observer("pack")).define("pack", ["d3", "width", "height"], function (d3, width, height) {
    return (
      data => d3.pack()
        .size([width - 2, height - 2])
        .padding(3)
        (d3.hierarchy(data)
          .sum(d => d.value)
          .sort((a, b) => b.value - a.value))
    )
  });
  main.variable(observer("width")).define("width", function () {
    return (
      900
    )
  });
  main.variable(observer("height")).define("height", ["width"], function (width) {
    return (
      width
    )
  });
  main.variable(observer("format")).define("format", ["d3"], function (d3) {
    return (
      d3.format(",d")
    )
  });
  main.variable(observer("color")).define("color", ["d3"], function (d3) {
    return (
      d3.scaleSequential([6, 0], d3.interpolateMagma)
    )
  });
  main.variable(observer("d3")).define("d3", ["require"], function (require) {
    return (
      require("d3@5")
    )
  });
  return main;
}
