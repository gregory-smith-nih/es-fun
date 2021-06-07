const glstools = require("glstools");
let files = glstools.files.readDir("docs");
for (let file of files) {
	let fullpath = "./docs/" + file;
	let infile = glstools.files.read(fullpath);
	let match = infile.match(/"active": false/);
	if (match) {
		//console.log(infile);
		let json = JSON.parse(infile);
		let resourcing = json._source.resourcing || [];
		for (let resource of resourcing) {
			console.log(resource);
		}
	}
}