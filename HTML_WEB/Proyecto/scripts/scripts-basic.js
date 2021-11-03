//
// Programmer:		Craig Stuart Sapp <craig@ccrma.stanford.edu>
// Creation Date:	Sun Oct 26 12:24:23 PDT 2014
// Last Modified:	Sun Oct 26 15:26:44 PDT 2014
// Filename:		.../scripts/scripts-basic.js
// Web Address:	https://josquin.stanford.edu/scripts-local.html
// Syntax:			JavaScript 1.8/ECMAScript 5; jQuery 2.0
// vim:				ts=3: ft=javascript
//
// Description:	Basic JavaScript utility functions for JRP pages
// 					which is loaded on all pages.
//


//////////////////////////////
//
// DOMContentLoaded event listener -- Things to do on a page after 
// 	the document has fininshed loading.
//

document.addEventListener('DOMContentLoaded', function() {
	StylizeFormElements();
	MakeNewLinkTargets();
}, false);



//////////////////////////////
//
// StylizeFormElements -- Apply CSS styling to form-like elements which
// 	are handled by the select2 and ezmark JavaScript libraries.
//

function StylizeFormElements() {
	$("select").not('.tricky').select2({
		width: "off"
	});

	$("select.tricky").select2({
		width: "off",
		containerCssClass: 'tricky-choice',
		dropdownCssClass: 'tricky-dropdown',
		dropdownAutoWidth: true
	});

	$('input[type=checkbox]').ezMark();
	$('input[type=radio]').ezMark();
}



///////////////////////////////
//
// MakeNewLinkTargets -- Assign a target to "new" for all <a> elements 
// 	in the document which are not relative.  If the link already
// 	has a target, then do not change it.
//

function MakeNewLinkTargets() {
	var alist = document.querySelectorAll("a");
	for (var i=0; i<alist.length; i++) {
		if (alist[i].getAttribute('target')) {
			continue;
		}
		var href = alist[i].getAttribute('href');
		if (!href) {
			continue;
		}
		if (href && !href.match(/^[A-Z-a-z]+:\/\//)) {
			continue;
		}
		alist[i].setAttribute('target', 'new');
	}
}



