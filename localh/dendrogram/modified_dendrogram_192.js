// for reference see https://observablehq.com/@d3/radial-dendrogram@192, this is a modified and stripped down version
export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["contract_address.json", new URL("./files/graph.json", import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], function (md) {
    return (
      md`# From files to actual results

This is a visual representation of the similarity graph, genereted using the .json created by SESC and D3’s [radial dendrogram](https://observablehq.com/@d3/radial-dendrogram).
As you can see the results are divided by matching percentage, the minimum level of similarity required is 70%. 
The number of results is currently limited to the best 200 matching contracts, in order to keep the  dendrogram readable.<br>
To view the source code of the central node click [here](http://localhost:8000/dendrogram/files/source.txt).`
    )
  });
  main.variable(observer("chart")).define("chart", ["tree", "d3", "data", "autoBox"], function (tree, d3, data, autoBox) {
    const root = tree(d3.hierarchy(data)
      .sort((a, b) => d3.ascending(a.data.name, b.data.name)));

    const svg = d3.create("svg");

    svg.append("g")
      .attr("fill", "none")
      .attr("stroke", "#555")
      .attr("stroke-opacity", 0.4)
      .attr("stroke-width", 1.5)
      .selectAll("path")
      .data(root.links())
      .join("path")
      .attr("d", d3.linkRadial()
        .angle(d => d.x)
        .radius(d => d.y));

    svg.append("g")
      .selectAll("circle")
      .data(root.descendants())
      .join("circle")
      .attr("transform", d => `
        rotate(${d.x * 180 / Math.PI - 90})
        translate(${d.y},0)
      `)
      .attr("fill", d => d.children ? "#555" : "#999")
      .attr("r", 2.5);

    svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("stroke-linejoin", "round")
      .attr("stroke-width", 3)
      .selectAll("text")
      .data(root.descendants())
      .join("text")
      .attr("transform", d => `
        rotate(${d.x * 180 / Math.PI - 90}) 
        translate(${d.y},0) 
        rotate(${d.x >= Math.PI ? 180 : 0})
      `)
      .attr("dy", "0.31em")
      .attr("x", d => d.x < Math.PI === !d.children ? 6 : -6)
      .attr("text-anchor", d => d.x < Math.PI === !d.children ? "start" : "end")
      .text(d => d.data.name)
      .clone(true).lower()
      .attr("stroke", "white");

    return svg.attr("viewBox", autoBox).node();
  }
  );
  main.variable(observer("autoBox")).define("autoBox", function () {
    return (
      function autoBox() {
        document.body.appendChild(this);
        const { x, y, width, height } = this.getBBox();
        document.body.removeChild(this);
        return [x, y, width, height];
      }
    )
  });
  main.variable(observer("data")).define("data", ["FileAttachment"], function (FileAttachment) {
    return (
      FileAttachment("contract_address.json").json()
    )
  });
  main.variable(observer("width")).define("width", function () {
    return (
      850
    )
  });
  main.variable(observer("radius")).define("radius", ["width"], function (width) {
    return (
      500
    )
  });
  main.variable(observer("tree")).define("tree", ["d3", "radius"], function (d3, radius) {
    return (
      d3.cluster().size([2 * Math.PI, radius - 100])
    )
  });
  main.variable(observer("d3")).define("d3", ["require"], function (require) {
    return (
      require("d3@5")
    )
  });
  return main;
}
