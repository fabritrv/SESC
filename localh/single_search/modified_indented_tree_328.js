//// for reference see https://observablehq.com/@d3/indented-tree@328, this is a modified and stripped down version
export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["results.json", new URL("./files/single_search.json", import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], function (md) {
    return (
      md`# Indented tree of your results

A better way to visualize your search results, genereted using the .json created by SESC and D3’s [indented tree](https://observablehq.com/@d3/indented-tree@328).
The tree also shows the number of results.`
    )
  });
  main.variable(observer("chart")).define("chart", ["root", "d3", "nodeSize", "width", "columns"], function (root, d3, nodeSize, width, columns) {
    const nodes = root.descendants();

    const svg = d3.create("svg")
      .attr("viewBox", [-nodeSize / 2, -nodeSize * 3 / 2, width, (nodes.length + 1) * nodeSize])
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .style("overflow", "visible");

    const link = svg.append("g")
      .attr("fill", "none")
      .attr("stroke", "#999")
      .selectAll("path")
      .data(root.links())
      .join("path")
      .attr("d", d => `
        M${d.source.depth * nodeSize},${d.source.index * nodeSize}
        V${d.target.index * nodeSize}
        h${nodeSize}
      `);

    const node = svg.append("g")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .attr("transform", d => `translate(0,${d.index * nodeSize})`);

    node.append("circle")
      .attr("cx", d => d.depth * nodeSize)
      .attr("r", 2.5)
      .attr("fill", d => d.children ? null : "#999");

    node.append("text")
      .attr("dy", "0.32em")
      .attr("x", d => d.depth * nodeSize + 6)
      .text(d => d.data.name);

    node.append("title")
      .text(d => d.ancestors().reverse().map(d => d.data.name).join("/"));

    for (const { label, value, format, x } of columns) {
      svg.append("text")
        .attr("dy", "0.32em")
        .attr("y", -nodeSize)
        .attr("x", x)
        .attr("text-anchor", "end")
        .attr("font-weight", "bold")
        .text(label);

      node.append("text")
        .attr("dy", "0.32em")
        .attr("x", x)
        .attr("text-anchor", "end")
        .attr("fill", d => d.children ? null : "#555")
        .attr("class", d => d.children ? null : "tohide")
        .data(root.copy().sum(value).descendants())
        .text(d => format(d.value, d));
    }

    return svg.node();
  }
  );
  main.variable(observer("columns")).define("columns", ["format"], function (format) {
    return (
      [
        {
          label: "Size",
          value: d => d.value,
          format,
          x: 280
        },
        {
          label: "Count",
          value: d => d.children ? 0 : 1,
          format: (value, d) => d.children ? format(value) : "-",
          x: 340
        }
      ]
    )
  });
  main.variable(observer("format")).define("format", ["d3"], function (d3) {
    return (
      d3.format(",")
    )
  });
  main.variable(observer("data")).define("data", ["FileAttachment"], function (FileAttachment) {
    return (
      FileAttachment("results.json").json()
    )
  });
  main.variable(observer("root")).define("root", ["d3", "data"], function (d3, data) { let i = 0; return d3.hierarchy(data).eachBefore(d => d.index = i++); }
  );
  main.variable(observer("nodeSize")).define("nodeSize", function () {
    return (
      17
    )
  });
  main.variable(observer("d3")).define("d3", ["require"], function (require) {
    return (
      require("d3@5")
    )
  });
  return main;
}
