/*
** THIS IS A TEST FILE FOR THE SPDX LICENSE DETECTION TESTS											
**																										
** This file has been auto generated using the SPDX License List as represented by
** the JSON files:  https://github.com/spdx/license-list-data 
** 
** This file is for test purposes only. It WILL NOT compile or do anything useful otherwise.
**
** Test File Version: 1.0 No SPDX Identifiers - License List version 2.6
**
** DISCLAIMER
**
** Any copyrights appearing in this test file do so because they were part of the license text as stored by SPDX and are included 
** only for test purposes as they are part of the license text.	They have no meaning, implied or specific, otherwise.	
*/




/*
** LICENSE HEADER AND COPYRIGHT TO DETECT	
** This section either uses either the standard license header, or if one does not exist, the license 
** text as shown on the SPDX License List. In addition, if the file was generated using the write 
** license identifiers option, they will appear before the license text.
** 										
**
** SPDX License to detect: https://spdx.org/licenses/LPPL-1.3a.html				
*/



/* SPDX-License-Identifier: LPPL-1.3a */
/*
Copyright <<var;name=copyright;original=2003 M. Y.
Name;match=.+>>

This work may be distributed and/or modified under
the conditions of the LaTeX Project Public License, either version 1.3
of this license or (at your option) any later version.

The latest
version of this license is
in
http://www.latex-project.org/lppl.txt
and version 1.3 or later is
part of all distributions of LaTeX version 2003/12/01 or later.

This
work has the LPPL maintenance status "maintained".
 
This Current
Maintainer of this work is <<var;name=maintainer;original=M. Y.
Name;match=.+>>.

This work consists of <<var;name=the
work;original=pig.dtx and pig.ins % and the derived file
pig.sty;match=.+>>.
*/

/*
** Fake code so we have something.
*/
#include <nothing.h>


int
noop_fun(int arg1)
{
	short retval;
	
	recalculatearg(&arg1);
	
	switch (arg1)
	{
		case 0:
			if (arg1) {
					retval = 1;
			} else {
			retval = 2;
			}
		case 1:
			retval = 2;
		case 2:
			retval = morpharg(arg1);
		case 3:
			if (arg1) {
				retval = 6;
			} else {
				retval = 7;
			}
		case 4:
			retval = upscalearg(arg1);
		default:
			retval = 0;
	}
	
	return retval;
}
