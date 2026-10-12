cd "..." /*Set your own folder path*/

****************************************************************************
/*Figure 1*/
****************************************************************************
clear
use data_gpt35_baseline

* add variables to xvars, controls
local xvars "minority ib2.igender ib2.igender#ib2.iethnicity"
local controls "worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree"
local i = 1

* generating three variables to store estimates, cilb, ciub of 95%
generate coefficient = .
generate cilb = .
generate ciub = .
generate order = .


local xvars_index = 1
local i = 1

* regression and extracting estimates, confidence intervals


foreach x in `xvars' {

    if `xvars_index' == 2 {
        local varlist "ib2.igender ib2.iethnicity"
    }
    else {
        local varlist `x'
    }

    eststo: reghdfe score_gpt35 `varlist' `controls', absorb(iposition istate last_work_title) vce(cluster iposition#istate)

    * retrieving the result
    matrix Result = r(table)

    forvalues j = 1/`xvars_index' {

        if `xvars_index' == 2 & `j' == 2 {
            replace coefficient = Result[1,3] in `i'
            replace cilb = Result[5,3] in `i'
            replace ciub = Result[6,3] in `i'
        }
        else {
            replace coefficient = Result[1,`j'] in `i'
            replace cilb = Result[5,`j'] in `i'
            replace ciub = Result[6,`j'] in `i'
        }

        replace order = 5.75 - `i' + 1 in `i'
        estimates store model`i'
        local i = `i' + 1

    }

    local xvars_index = `xvars_index' + 1

}




* Set scheme and graph coefplot
set scheme s1color

* graphing
graph twoway (rspike cilb ciub order, horizontal lwidth(medium) lcolor(black%75) lpattern(dash)) ///
				(scatter order coefficient, msize(medsmall) mcolor("0 183 255") msymbol(diamond)), ///
				ylabel(5.75 "Minority" ///
				4.75 "Female" ///
				3.75 "Black" ///
				2.75 "Female & Black" ///
				1.75 "Female & White" ///
				0.75 "Male & Black" ///
				, labsize(small) angle(0) nogrid) ///
				ytitle("") ///
				xtitle("Coefficient") ///
				xlabel(-0.3(0.25)0.7, labsize(small)) ///
				xline(0, lpattern(dot)) ///
				yline(5.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				yline(3.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				title() ///
				legend(off) ///
				text(5.66 0.0995 "0.0995", place(s) size(tiny)) ///
				text(5.66 0.0026 "0.0026", place(s) size(tiny)) ///
				text(5.66 0.1963 "0.1963", place(s) size(tiny)) ///
				text(4.66 0.4521 "0.4521", place(s) size(tiny)) ///
				text(4.66 0.3892 "0.3892", place(s) size(tiny)) ///
				text(4.66 0.5151 "0.5151", place(s) size(tiny)) ///
				text(3.66 -0.0736 "-0.0736", place(s) size(tiny)) ///
				text(3.66 -0.1597 "-0.1597", place(s) size(tiny)) ///
				text(3.66 0.0125 "0.0125", place(s) size(tiny)) ///
				text(2.66 0.3786 "0.3786", place(s) size(tiny)) ///
				text(2.66 0.2784 "0.2784", place(s) size(tiny)) ///
				text(2.66 0.4789 "0.4789", place(s) size(tiny)) ///
				text(1.66 0.2227 "0.2227", place(s) size(tiny)) ///
				text(1.66 0.1062 "0.1062", place(s) size(tiny)) ///
				text(1.66 0.3392 "0.3392", place(s) size(tiny)) ///
				text(0.71 -0.3032 "-0.3032", place(s) size(tiny)) ///
				text(0.71 -0.4323 "-0.4323", place(s) size(tiny)) ///
				text(0.71 -0.1741 "-0.1741", place(s) size(tiny))

* save graph
graph save Figure1.gph, replace
graph export Figure1.eps, as(eps) replace

****************************************************************************
/*Figure 2*/
****************************************************************************
clear
use data_gpt35_heter

* Initialize variables to store estimates and confidence intervals
generate coefficient_high = .
generate coefficient_low = .
generate cilb_high = .
generate cilb_low = .
generate ciub_high = .
generate ciub_low = .
generate order_high = .
generate order_low = .


/*Figure 3a*/
local i = 1

* Loop through xvars and subs
foreach regtype in "ib2.igender ib2.iethnicity" "ib2.igender ib2.iethnicity" "ib2.igender#ib2.iethnicity" "ib2.igender#ib2.iethnicity" "ib2.igender#ib2.iethnicity" {
    foreach mf_bls in 1 0 {       
		reghdfe score_gpt35 `regtype' worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree if median_female_bls==`mf_bls', absorb(iposition istate last_work_title) cluster(iposition#istate) 
		local coef = cond(`mf_bls' == 1, "high", "low")
		local result_col = cond(`i' < 3 | `i' == 5 | `i' == 6, 1, cond(`i' == 7 | `i' == 8, 2, 3))

		matrix Result =  r(table)
		replace coefficient_`coef' = Result[1,`result_col'] in `i'
		replace cilb_`coef' = Result[5,`result_col'] in `i'
		replace ciub_`coef' = Result[6,`result_col'] in `i'
		
		local m = ceil(`i' / 2)
		replace order_`coef' = 5.75 - `m' + cond(`mf_bls' == 1, 0.08, -0.08) in `i'

		estimates store model`i'
		local i = `i' + 1
        
    }
}

* Set scheme and graph coefplot
set scheme s1color

* graphing				
graph twoway (rspike cilb_high ciub_high order_high, horizontal lwidth(medium) lcolor(black%75) lpattern(dash)) ///
				(rspike cilb_low ciub_low order_low, horizontal lwidth(medium) lcolor(black%75) lpattern(dash)) ///
				(scatter order_high coefficient_high, msize(medsmall) mcolor("255 83 0") msymbol(diamond)) ///
				(scatter order_low coefficient_low, msize(medsmall) mcolor("0 183 255") msymbol(round)), ///
				ylabel(4.75 "Female" ///
				3.75 "Black" ///
				2.75 "Female & Black" ///
				1.75 "Female & White" /// 
				0.75 "Male & Black" ///
				, labsize(small) angle(0) nogrid) ///
				ytitle("") ///
				xtitle("") ///
				xlabel(-0.7(0.1)0.6, labsize(small)) ///
				xline(0, lpattern(dot)) ///
				yline(3.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				title(Score by National Share of Female in the Position, size(small)) ///
				legend(order(3 "High" 4 "Low")) ///
				text(5.2 -1.05 "A", tstyle(heading) size(5) place(e))

* save graph
graph save figure_2a.gph, replace
graph export figure_2a.png, as(png) replace


/*Figure 2b*/
local i = 1

* Loop through xvars and subs
foreach regtype in "ib2.igender ib2.iethnicity" "ib2.igender ib2.iethnicity" "ib2.igender#ib2.iethnicity" "ib2.igender#ib2.iethnicity" "ib2.igender#ib2.iethnicity" {
    foreach mf_bls in 1 0 {       
		reghdfe score_gpt35 `regtype' worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree if median_black_bls==`mf_bls', absorb(iposition istate last_work_title) cluster(iposition#istate) 
		local coef = cond(`mf_bls' == 1, "high", "low")
		local result_col = cond(`i' < 3 | `i' == 5 | `i' == 6, 1, cond(`i' == 7 | `i' == 8, 2, 3))

		matrix Result =  r(table)
		replace coefficient_`coef' = Result[1,`result_col'] in `i'
		replace cilb_`coef' = Result[5,`result_col'] in `i'
		replace ciub_`coef' = Result[6,`result_col'] in `i'
		
		local m = ceil(`i' / 2)
		replace order_`coef' = 5.75 - `m' + cond(`mf_bls' == 1, 0.08, -0.08) in `i'

		estimates store model`i'
		local i = `i' + 1
        
    }
}

* Set scheme and graph coefplot
set scheme s1color

* graphing				
graph twoway (rspike cilb_high ciub_high order_high, horizontal lwidth(medium) lcolor(black%75) lpattern(dash)) ///
				(rspike cilb_low ciub_low order_low, horizontal lwidth(medium) lcolor(black%75) lpattern(dash)) ///
				(scatter order_high coefficient_high, msize(medsmall) mcolor("255 83 0") msymbol(diamond)) ///
				(scatter order_low coefficient_low, msize(medsmall) mcolor("0 183 255") msymbol(round)), ///
				ylabel(4.75 "Female" ///
				3.75 "Black" ///
				2.75 "Female & Black" ///
				1.75 "Female & White" /// 
				0.75 "Male & Black" ///
				, labsize(small) angle(0) nogrid) ///
				ytitle("") ///
				xtitle("") ///
				xlabel(-0.7(0.1)0.6, labsize(small)) ///
				xline(0, lpattern(dot)) ///
				yline(3.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				title(Score by National Share of Black in the Position, size(small)) ///
				legend(order(3 "High" 4 "Low")) ///
				text(5.2 -1.05 "B", tstyle(heading) size(5) place(e))				
				
* save graph
graph save figure_2b.gph, replace
graph export figure_2b.png, as(png) replace

/*Figure 3c*/
gen red=inlist(istate,2,3,5)
generate coefficient_red = .
generate coefficient_blue = .
generate cilb_red = .
generate cilb_blue = .
generate ciub_red = .
generate ciub_blue = .
generate order_red = .
generate order_blue = .

local i = 1
* Loop through xvars and subs
foreach regtype in "minority" "ib2.igender ib2.iethnicity" "ib2.igender ib2.iethnicity" "ib2.igender#ib2.iethnicity" "ib2.igender#ib2.iethnicity" "ib2.igender#ib2.iethnicity" {
    foreach mf_bls in 1 0 {       
		reghdfe score_gpt35 `regtype' worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree if red==`mf_bls', absorb(iposition istate last_work_title) cluster(iposition#istate) 
		local coef = cond(`mf_bls' == 1, "red", "blue")
		local result_col = cond(`i' < 5, 1, cond(`i' >= 5 & `i' <= 6, 3, cond(`i' >= 7 & `i' <= 8, 1, cond(`i' >= 9 & `i' <= 10, 2, 3))))

		matrix Result =  r(table)
		replace coefficient_`coef' = Result[1,`result_col'] in `i'
		replace cilb_`coef' = Result[5,`result_col'] in `i'
		replace ciub_`coef' = Result[6,`result_col'] in `i'
		
		local m = ceil(`i' / 2)
		replace order_`coef' = 6.75 - `m' + cond(`mf_bls' == 1, 0.08, -0.08) in `i'

		estimates store model`i'
		local i = `i' + 1
        
    }
}

* Set scheme and graph coefplot
set scheme s1color

* graphing				
graph twoway (rspike cilb_red ciub_red order_red, horizontal lwidth(medium) lcolor(black%75) lpattern(dash)) ///
				(rspike cilb_blue ciub_blue order_blue, horizontal lwidth(medium) lcolor(black%75) lpattern(dash)) ///
				(scatter order_red coefficient_red, msize(medsmall) mcolor("255 83 0") msymbol(diamond)) ///
				(scatter order_blue coefficient_blue, msize(medsmall) mcolor("0 183 255") msymbol(round)), ///
				ylabel(5.75 "Minority" ///
				4.75 "Female" ///
				3.75 "Black" ///
				2.75 "Female & Black" ///
				1.75 "Female & White" /// 
				0.75 "Male & Black" ///
				, labsize(small) angle(0) nogrid) ///
				ytitle("") ///
				xtitle("") ///
				xlabel(-0.7(0.1)0.6, labsize(small)) ///
				xline(0, lpattern(dot)) ///
				yline(5.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				yline(3.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				title(Score by Political Orientation of the State, size(small)) ///
				legend(order(3 "Republican" 4 "Democratic")) ///
				text(6.45 -1.05 "C", tstyle(heading) size(5) place(e)) 				
				
* save graph
graph save figure_2c.gph, replace
graph export figure_2c, as(png) replace

* --------------
* Combine
* --------------
resizecombine "figure_2a.gph" "figure_2b.gph" "figure_2c.gph", ///
cols(1) ysize(45cm) xsize(20cm) imargin(10 10 10 10)

graph save "Figure2.gph", replace
graph export Figure2.eps, as(eps) replace

****************************************************************************
/*Figure 3*/
/*
For this figure, we manually store the bootstrapped results to a data file,
based on which we plot the figure.
*/
****************************************************************************

/****Bootstrap****/
/*
The results running the bootstrapping codes can be slightly different from 
those in the figure, as each time the random simulation can generate slightly 
different results.
*/
clear
use data_gpt35_baseline

****
set matsize 10000

matrix R=J(500,6,.)
forval p=1/500{
display "Sampling `p'"
cap drop isampling
gen isampling=uniform()
qui reghdfe score_gpt35 minority worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree if isampling<.2, absorb(iposition istate last_work_title) cluster(iposition#istate)
matrix RP=r(table)
foreach x in 1{
matrix R[`p'-1+`x',1]=`p'
matrix R[`p'-1+`x',2]=RP[1,`x']
matrix R[`p'-1+`x',3]=RP[2,`x']
matrix R[`p'-1+`x',4]=RP[4,`x']
matrix R[`p'-1+`x',5]=RP[5,`x']
matrix R[`p'-1+`x',6]=RP[6,`x']
}
}
matrix list R

matrix R=J(1000,6,.)
forval p=1/500{
display "Sampling `p'"
cap drop isampling
gen isampling=uniform()
qui reghdfe score_gpt35 ib2.igender ib2.iethnicity worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree if isampling<.2, absorb(iposition istate last_work_title) cluster(iposition#istate)
matrix RP=r(table)
local x=0
foreach k in 1 3{
local x=`x'+1
matrix R[`p'*2-2+`x',1]=`p'
matrix R[`p'*2-2+`x',2]=RP[1,`k']
matrix R[`p'*2-2+`x',3]=RP[2,`k']
matrix R[`p'*2-2+`x',4]=RP[4,`k']
matrix R[`p'*2-2+`x',5]=RP[5,`k']
matrix R[`p'*2-2+`x',6]=RP[6,`k']
}
}
matrix list R

matrix R=J(1500,6,.)
forval p=1/500{
display "Sampling `p'"
cap drop isampling
gen isampling=uniform()
qui reghdfe score_gpt35 ib2.igender#ib2.iethnicity worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree if isampling<.2, absorb(iposition istate last_work_title) cluster(iposition#istate)
matrix RP=r(table)
local x=0
foreach k in 1 2 3{
local x=`x'+1
matrix R[`p'*3-3+`x',1]=`p'
matrix R[`p'*3-3+`x',2]=RP[1,`k']
matrix R[`p'*3-3+`x',3]=RP[2,`k']
matrix R[`p'*3-3+`x',4]=RP[4,`k']
matrix R[`p'*3-3+`x',5]=RP[5,`k']
matrix R[`p'*3-3+`x',6]=RP[6,`k']
}
}
matrix list R

/****Figure****/
clear
use data_bootstrap_gpt35

* --------------
* GRAPH A
* --------------
preserve
keep if gpt35_base == "Minority"

quietly summarize b
local mean = r(mean)

histogram b, title("Minority") ylabel(,nogrid) ytitle("Percentage", size(large)) percent lcolor(gs12) fcolor(sandb%70) lwidth(thin) plotregion(color(white)) xtitle("") graphregion(color(white)) bgcolor(white) legend(off) ///
xline(`mean', lcolor(red) lpattern(dash)) ///
text(16.5 -0.14 "A", size(5))

graph save Graph3a.gph, replace
graph export Graph3a.png, replace
   
restore

* --------------
* GRAPH B
* --------------
preserve
keep if gpt35_base == "Female"

quietly summarize b
local mean = r(mean)

histogram b, title("Female") ylabel(,nogrid) ytitle("Percentage", size(large)) percent lcolor(gs12) fcolor(sandb%70) lwidth(thin) plotregion(color(white)) xtitle("") graphregion(color(white)) bgcolor(white) legend(off) ///
xline(`mean', lcolor(red) lpattern(dash)) ///
text(16.5 0.27 "B", size(5))

graph save Graph3b.gph, replace
graph export Graph3b.png, replace

restore

* --------------
* GRAPH C
* --------------
preserve
keep if gpt35_base == "Black"

quietly summarize b
local mean = r(mean)

histogram b, title("Black") ylabel(,nogrid) ytitle("Percentage", size(large)) percent lcolor(gs12) fcolor(sandb%70) lwidth(thin) plotregion(color(white)) xtitle("") graphregion(color(white)) bgcolor(white) legend(off) ///
xline(`mean', lcolor(red) lpattern(dash)) ///
text(16.5 -0.24 "C", size(5))

graph save Graph3c.gph, replace
graph export Graph3c.png, replace
  
restore

* --------------
* GRAPH D
* --------------
preserve
keep if gpt35_base == "Female & Black"

quietly summarize b
local mean = r(mean)

histogram b, title("Female & Black") ylabel(,nogrid) ytitle("Percentage", size(large)) percent lcolor(gs12) fcolor(sandb%70) lwidth(thin) plotregion(color(white)) xtitle("") graphregion(color(white)) bgcolor(white) legend(off) ///
xline(`mean', lcolor(red) lpattern(dash)) ///
text(16.5 0.05 "D", size(5))

graph save Graph3d.gph, replace
graph export Graph3d.png, replace
   
restore

* --------------
* GRAPH E
* --------------
preserve
keep if gpt35_base == "Female & White"

quietly summarize b
local mean = r(mean)

histogram b, title("Female & White") ylabel(,nogrid) ytitle("Percentage", size(large)) percent lcolor(gs12) fcolor(sandb%70) lwidth(thin) plotregion(color(white)) xtitle("") graphregion(color(white)) bgcolor(white) legend(off) ///
xline(`mean', lcolor(red) lpattern(dash)) ///
text(16.5 -0.09 "E", size(5))

graph save Graph3e.gph, replace
graph export Graph3e.png, replace
  
restore

* --------------
* GRAPH F
* --------------
preserve
keep if gpt35_base == "Male & Black"

quietly summarize b
local mean = r(mean)

histogram b, title("Male & Black") ylabel(,nogrid) ytitle("Percentage", size(large)) percent lcolor(gs12) fcolor(sandb%70) lwidth(thin) plotregion(color(white)) xtitle("") graphregion(color(white)) bgcolor(white) legend(off) ///
xline(`mean', lcolor(red) lpattern(dash)) ///
text(16.5 -0.56 "F", size(5))

graph save Graph3f.gph, replace
graph export Graph3f.png, replace

restore

* --------------
* Combine
* --------------

resizecombine "Graph3a.gph" "Graph3b.gph" "Graph3c.gph" "Graph3d.gph" "Graph3e.gph" "Graph3f.gph", ///
cols(3) ysize(20cm) xsize(28cm) imargin(5 5 5 5)

graph save "Figure3.gph", replace
graph export Figure3.eps, as(eps) replace

****************************************************************************
/*Figure 4*/
/*
For this figure, we manually store the estimated results to a data file,
based on which we plot the figure.
*/
****************************************************************************

/****Econ magnitude****/
clear
use data_gpt35_baseline

****
matrix R=J(6,6,.)
local p=0
foreach cutoff in 60 65 70 75 80 85{
local p=`p'+1
cap drop y_cut
gen y_cut=(score_gpt35>=`cutoff') if score_gpt35<.
qui reghdfe y_cut minority worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree, absorb(iposition istate last_work_title) cluster(iposition#istate)
matrix RP=r(table)
foreach x in 1{
matrix R[`p'-1+`x',1]=`p'
matrix R[`p'-1+`x',2]=RP[1,`x']
matrix R[`p'-1+`x',3]=RP[2,`x']
matrix R[`p'-1+`x',4]=RP[4,`x']
matrix R[`p'-1+`x',5]=RP[5,`x']
matrix R[`p'-1+`x',6]=RP[6,`x']
}
}
matrix list R

****
matrix R=J(12,6,.)
local p=0
foreach cutoff in 60 65 70 75 80 85{
local p=`p'+1
cap drop y_cut
gen y_cut=(score_gpt35>=`cutoff') if score_gpt35<.
qui reghdfe y_cut ib2.igender ib2.iethnicity worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree, absorb(iposition istate last_work_title) cluster(iposition#istate)
matrix RP=r(table)
local x=0
foreach k in 1 3{
local x=`x'+1
matrix R[`p'*2-2+`x',1]=`p'
matrix R[`p'*2-2+`x',2]=RP[1,`k']
matrix R[`p'*2-2+`x',3]=RP[2,`k']
matrix R[`p'*2-2+`x',4]=RP[4,`k']
matrix R[`p'*2-2+`x',5]=RP[5,`k']
matrix R[`p'*2-2+`x',6]=RP[6,`k']
}
}
matrix list R

****
matrix R=J(18,6,.)
local p=0
foreach cutoff in 60 65 70 75 80 85{
local p=`p'+1
cap drop y_cut
gen y_cut=(score_gpt35>=`cutoff') if score_gpt35<.
qui reghdfe y_cut ib2.igender#ib2.iethnicity worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree, absorb(iposition istate last_work_title) cluster(iposition#istate)
matrix RP=r(table)
local x=0
foreach k in 1 2 3{
local x=`x'+1
matrix R[`p'*3-3+`x',1]=`p'
matrix R[`p'*3-3+`x',2]=RP[1,`k']
matrix R[`p'*3-3+`x',3]=RP[2,`k']
matrix R[`p'*3-3+`x',4]=RP[4,`k']
matrix R[`p'*3-3+`x',5]=RP[5,`k']
matrix R[`p'*3-3+`x',6]=RP[6,`k']
}
}
matrix list R


/****Econ magnitude****/
clear
use data_magnitude_gpt35

* Set scheme and graph coefplot
set scheme s1color

* graphing
graph twoway (rspike cilb_a ciub_a order_a, vertical lwidth(medium) lcolor(black%75) lpattern(dash)) ///
             (rspike cilb_b ciub_b order_b, vertical lwidth(medium) lcolor(black%75) lpattern(dash)) ///
             (rspike cilb_c ciub_c order_c, vertical lwidth(medium) lcolor(black%75) lpattern(dash)) ///
             (rspike cilb_d ciub_d order_d, vertical lwidth(medium) lcolor(black%75) lpattern(dash)) ///
             (rspike cilb_e ciub_e order_e, vertical lwidth(medium) lcolor(black%75) lpattern(dash)) ///
             (rspike cilb_f ciub_f order_f, vertical lwidth(medium) lcolor(black%75) lpattern(dash)) ///
             (scatter coefficient_a order_a, msize(medsmall) mcolor("255 83 0") msymbol(diamond)) ///
             (scatter coefficient_b order_b, msize(medsmall) mcolor("0 183 255") msymbol(round)) ///
             (scatter coefficient_c order_c, msize(medsmall) mcolor("0 183 55") msymbol(square)) ///
             (scatter coefficient_d order_d, msize(medsmall) mcolor("128 0 128") msymbol(triangle)) /// 紫色
             (scatter coefficient_e order_e, msize(medsmall) mcolor("255 165 0") msymbol(x)) /// 橙色
             (scatter coefficient_f order_f, msize(medsmall) mcolor("0 128 0") msymbol(plus)), /// 绿色
             xlabel(5.75 ">=85" ///
                    4.75 ">=80" ///
                    3.75 ">=75" ///
                    2.75 ">=70" ///
                    1.75 ">=65" ///
                    0.75 ">=60", ///
                    labsize(small) angle(0) nogrid) ///
             ytitle("") ///
             xtitle("") ///
             ylabel(-0.02(0.005)0.03, labsize(small)) ///
             yline(0, lpattern(dot)) ///
             legend(order(7 8 9 10 11 12) label(7 "Minority") label(8 "Female") label(9 "Black") label(10 "Female & Black") label(11 "Female & White") label(12 "Male & Black") rows(1) size(small))

* save graph
graph save Figure4.gph, replace
graph export Figure4.eps, as(eps) replace

****************************************************************************
/*Figure 5*/
****************************************************************************
clear
use data_score_4models

* --------------
* GRAPH A
* --------------
* add variables to xvars, controls
local xvars "minority ib2.igender ib2.igender#ib2.iethnicity"
local controls "worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree"
local i = 1

* generating three variables to store estimates, cilb, ciub of 95%
generate coefficient = .
generate cilb = .
generate ciub = .
generate order = .


local xvars_index = 1
local i = 1

* regression and extracting estimates, confidence intervals
foreach x in `xvars' {

    if `xvars_index' == 2 {
        local varlist "ib2.igender ib2.iethnicity"
    }
    else {
        local varlist `x'
    }

    eststo: reghdfe score_gpt4o `varlist' `controls', absorb(iposition istate last_work_title) vce(cluster iposition#istate)

    * retrieving the result
    matrix Result = r(table)

    forvalues j = 1/`xvars_index' {

        if `xvars_index' == 2 & `j' == 2 {
            replace coefficient = Result[1,3] in `i'
            replace cilb = Result[5,3] in `i'
            replace ciub = Result[6,3] in `i'
        }
        else {
            replace coefficient = Result[1,`j'] in `i'
            replace cilb = Result[5,`j'] in `i'
            replace ciub = Result[6,`j'] in `i'
        }

        replace order = 5.75 - `i' + 1 in `i'
        estimates store model`i'
        local i = `i' + 1

    }

    local xvars_index = `xvars_index' + 1

}


* Set scheme and graph coefplot
set scheme s1color

* graphing
graph twoway (rspike cilb ciub order, horizontal lwidth(medium) lcolor(black%75) lpattern(dash)) ///
				(scatter order coefficient, msize(medsmall) mcolor("0 183 255") msymbol(diamond)), ///
				ylabel(5.75 "Minority" ///
				4.75 "Female" ///
				3.75 "Black" ///
				2.75 "Female & Black" ///
				1.75 "Female & White" ///
				0.75 "Male & Black" ///
				, labsize(small) angle(0) nogrid) ///
				ytitle("") ///
				xtitle("Coefficient") ///
				xlabel(-0.75(0.25)0.75, labsize(small)) ///
				xline(0, lpattern(dot)) ///
				yline(5.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				yline(3.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				title(Scores by GPT-4o) ///
				legend(off) ///
				text(5.66 0.0367 "0.0367", place(s) size(tiny)) ///
				text(5.66 -0.0989 "-0.0989", place(s) size(tiny)) ///
				text(5.66 0.1722 "0.1722", place(s) size(tiny)) ///
				text(4.66 0.6455 "0.6455", place(s) size(tiny)) ///
				text(4.66 0.5373 "0.5373", place(s) size(tiny)) ///
				text(4.66 0.7537 "0.7537", place(s) size(tiny)) ///
				text(3.66 -0.2320 "-0.2320", place(s) size(tiny)) ///
				text(3.66 -0.3233 "-0.3233", place(s) size(tiny)) ///
				text(3.66 -0.1406 "-0.1406", place(s) size(tiny)) ///
				text(2.66 0.4139 "0.4139", place(s) size(tiny)) ///
				text(2.66 0.2663 "0.2663", place(s) size(tiny)) ///
				text(2.66 0.5614 "0.5614", place(s) size(tiny)) ///
				text(1.66 0.2868 "0.2868", place(s) size(tiny)) ///
				text(1.66 0.1253 "0.1253", place(s) size(tiny)) ///
				text(1.66 0.4484 "0.4484", place(s) size(tiny)) ///
				text(0.71 -0.5907 "-0.5907", place(s) size(tiny)) ///
				text(0.71 -0.7478 "-0.7478", place(s) size(tiny)) ///
				text(0.71 -0.4335 "-0.4335", place(s) size(tiny)) ///
				text(6.25 -1.1 "A", tstyle(heading) size(5) place(e)) 

* save graph
graph save figure_gpt4o.gph, replace
graph export figure_gpt4o.png, as(png) replace


* --------------
* GRAPH B
* --------------
* add variables to xvars, controls
local xvars "minority ib2.igender ib2.igender#ib2.iethnicity"
local controls "worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree"
local i = 1

local xvars_index = 1
local i = 1

* regression and extracting estimates, confidence intervals
foreach x in `xvars' {

    if `xvars_index' == 2 {
        local varlist "ib2.igender ib2.iethnicity"
    }
    else {
        local varlist `x'
    }

    eststo: reghdfe score_gemini `varlist' `controls', absorb(iposition istate last_work_title) vce(cluster iposition#istate)

    * retrieving the result
    matrix Result = r(table)

    forvalues j = 1/`xvars_index' {

        if `xvars_index' == 2 & `j' == 2 {
            replace coefficient = Result[1,3] in `i'
            replace cilb = Result[5,3] in `i'
            replace ciub = Result[6,3] in `i'
        }
        else {
            replace coefficient = Result[1,`j'] in `i'
            replace cilb = Result[5,`j'] in `i'
            replace ciub = Result[6,`j'] in `i'
        }

        replace order = 5.75 - `i' + 1 in `i'
        estimates store model`i'
        local i = `i' + 1

    }

    local xvars_index = `xvars_index' + 1

}

* Set scheme and graph coefplot
set scheme s1color

* graphing
graph twoway (rspike cilb ciub order, horizontal lwidth(medium) lcolor(black%75) lpattern(dash)) ///
				(scatter order coefficient, msize(medsmall) mcolor("0 183 255") msymbol(diamond)), ///
				ylabel(5.75 "Minority" ///
				4.75 "Female" ///
				3.75 "Black" ///
				2.75 "Female & Black" ///
				1.75 "Female & White" ///
				0.75 "Male & Black" ///
				, labsize(small) angle(0) nogrid) ///
				ytitle("") ///
				xtitle("Coefficient") ///
				xlabel(-0.5(0.25)1.25, labsize(small)) ///
				xline(0, lpattern(dot)) ///
				yline(5.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				yline(3.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				title(Scores by Gemini 1.5 Flash) ///
				legend(off) ///
				text(5.66 0.5107 "0.5107", place(s) size(tiny)) ///
				text(5.66 0.3848 "0.3848", place(s) size(tiny)) ///
				text(5.66 0.6366 "0.6366", place(s) size(tiny)) ///
				text(4.66 1.0174 "1.0174", place(s) size(tiny)) ///
				text(4.66 0.9032 "0.9032", place(s) size(tiny)) ///
				text(4.66 1.1315 "1.1315", place(s) size(tiny)) ///
				text(3.66 -0.0613 "-0.0613", place(s) size(tiny)) ///
				text(3.66 -0.1563 "-0.1563", place(s) size(tiny)) ///
				text(3.66 0.0337 "0.0337", place(s) size(tiny)) ///
				text(2.66 0.9560 "0.9560", place(s) size(tiny)) ///
				text(2.66 0.8284 "0.8284", place(s) size(tiny)) ///
				text(2.66 1.0836 "1.0836", place(s) size(tiny)) ///
				text(1.66 0.8271 "0.8271", place(s) size(tiny)) ///
				text(1.66 0.6649 "0.6649", place(s) size(tiny)) ///
				text(1.66 0.9894 "0.9894", place(s) size(tiny)) ///
				text(0.71 -0.2517 "-0.2517", place(s) size(tiny)) ///
				text(0.71 -0.4124 "-0.4124", place(s) size(tiny)) ///
				text(0.71 -0.0909 "-0.0909", place(s) size(tiny)) ///
				text(6.25 -0.95 "B", tstyle(heading) size(5) place(e)) 

* save graph
graph save figure_gemini.gph, replace
graph export figure_gemini.png, as(png) replace


* --------------
* GRAPH C
* --------------
* add variables to xvars, controls
local xvars "minority ib2.igender ib2.igender#ib2.iethnicity"
local controls "worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree"
local i = 1

local xvars_index = 1
local i = 1

* regression and extracting estimates, confidence intervals


foreach x in `xvars' {

    if `xvars_index' == 2 {
        local varlist "ib2.igender ib2.iethnicity"
    }
    else {
        local varlist `x'
    }

    eststo: reghdfe score_claude `varlist' `controls', absorb(iposition istate last_work_title) vce(cluster iposition#istate)

    * retrieving the result
    matrix Result = r(table)

    forvalues j = 1/`xvars_index' {

        if `xvars_index' == 2 & `j' == 2 {
            replace coefficient = Result[1,3] in `i'
            replace cilb = Result[5,3] in `i'
            replace ciub = Result[6,3] in `i'
        }
        else {
            replace coefficient = Result[1,`j'] in `i'
            replace cilb = Result[5,`j'] in `i'
            replace ciub = Result[6,`j'] in `i'
        }

        replace order = 5.75 - `i' + 1 in `i'
        estimates store model`i'
        local i = `i' + 1

    }

    local xvars_index = `xvars_index' + 1

}


* Set scheme and graph coefplot
set scheme s1color

* graphing
graph twoway (rspike cilb ciub order, horizontal lwidth(medium) lcolor(black%75) lpattern(dash)) ///
				(scatter order coefficient, msize(medsmall) mcolor("0 183 255") msymbol(diamond)), ///
				ylabel(5.75 "Minority" ///
				4.75 "Female" ///
				3.75 "Black" ///
				2.75 "Female & Black" ///
				1.75 "Female & White" ///
				0.75 "Male & Black" ///
				, labsize(small) angle(0) nogrid) ///
				ytitle("") ///
				xtitle("Coefficient") ///
				xlabel(-0.85(0.25)1.15, labsize(small)) ///
				xline(0, lpattern(dot)) ///
				yline(5.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				yline(3.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				title(Scores by Claude 3.5 Sonnet) ///
				legend(off) ///
				text(5.66 0.3336 "0.3336", place(s) size(tiny)) ///
				text(5.66 0.1999 "0.1999", place(s) size(tiny)) ///
				text(5.66 0.4673 "0.4673", place(s) size(tiny)) ///
				text(4.66 1.1098 "1.1098", place(s) size(tiny)) ///
				text(4.66 0.9535 "0.9535", place(s) size(tiny)) ///
				text(4.66 1.2660 "1.2660", place(s) size(tiny)) ///
				text(3.66 -0.3996 "-0.3996", place(s) size(tiny)) ///
				text(3.66 -0.5 "-0.4725", place(s) size(tiny)) ///
				text(3.66 -0.3 "-0.3268", place(s) size(tiny)) ///
				text(2.66 0.7098 "0.7098", place(s) size(tiny)) ///
				text(2.66 0.5366 "0.5366", place(s) size(tiny)) ///
				text(2.66 0.8831 "0.8831", place(s) size(tiny)) ///
				text(1.66 0.8983 "0.8983", place(s) size(tiny)) ///
				text(1.66 0.7233 "0.7233", place(s) size(tiny)) ///
				text(1.66 1.0733 "1.0733", place(s) size(tiny)) ///
				text(0.71 -0.6114 "-0.6114", place(s) size(tiny)) ///
				text(0.71 -0.7353 "-0.7353", place(s) size(tiny)) ///
				text(0.71 -0.4875 "-0.4875", place(s) size(tiny)) ///
				text(6.25 -1.4 "C", tstyle(heading) size(5) place(e)) 

* save graph
graph save figure_claude.gph, replace
graph export figure_claude.png, as(png) replace


* --------------
* GRAPH D
* --------------
* add variables to xvars, controls
local xvars "minority ib2.igender ib2.igender#ib2.iethnicity"
local controls "worknum edunum skillnum num_high_level avg_duration_work first_work_start avg_length_work_desc duration_edu first_edu_start i.highest_degree"
local i = 1

local xvars_index = 1
local i = 1

* regression and extracting estimates, confidence intervals


foreach x in `xvars' {

    if `xvars_index' == 2 {
        local varlist "ib2.igender ib2.iethnicity"
    }
    else {
        local varlist `x'
    }

    eststo: reghdfe score_llama `varlist' `controls', absorb(iposition istate last_work_title) vce(cluster iposition#istate)

    * retrieving the result
    matrix Result = r(table)

    forvalues j = 1/`xvars_index' {

        if `xvars_index' == 2 & `j' == 2 {
            replace coefficient = Result[1,3] in `i'
            replace cilb = Result[5,3] in `i'
            replace ciub = Result[6,3] in `i'
        }
        else {
            replace coefficient = Result[1,`j'] in `i'
            replace cilb = Result[5,`j'] in `i'
            replace ciub = Result[6,`j'] in `i'
        }

        replace order = 5.75 - `i' + 1 in `i'
        estimates store model`i'
        local i = `i' + 1

    }

    local xvars_index = `xvars_index' + 1

}

* Set scheme and graph coefplot
set scheme s1color

* graphing
graph twoway (rspike cilb ciub order, horizontal lwidth(medium) lcolor(black%75) lpattern(dash)) ///
				(scatter order coefficient, msize(medsmall) mcolor("0 183 255") msymbol(diamond)), ///
				ylabel(5.75 "Minority" ///
				4.75 "Female" ///
				3.75 "Black" ///
				2.75 "Female & Black" ///
				1.75 "Female & White" ///
				0.75 "Male & Black" ///
				, labsize(small) angle(0) nogrid) ///
				ytitle("") ///
				xtitle("Coefficient") ///
				xlabel(-0.3(0.25)1.2, labsize(small)) ///
				xline(0, lpattern(dot)) ///
				yline(5.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				yline(3.25, lpattern(dash) lcolor(orange) lwidth(thick)) ///
				title(Scores by Llama 3-70b) ///
				legend(off) ///
				text(5.66 0.4300 "0.4300", place(s) size(tiny)) ///
				text(5.66 0.2700 "0.2700", place(s) size(tiny)) ///
				text(5.66 0.5901 "0.5901", place(s) size(tiny)) ///
				text(4.66 0.7488 "0.7488", place(s) size(tiny)) ///
				text(4.66 0.5639 "0.5639", place(s) size(tiny)) ///
				text(4.66 0.9337 "0.9337", place(s) size(tiny)) ///
				text(3.66 0.1482 "0.1482", place(s) size(tiny)) ///
				text(3.66 0.0272 "0.0272", place(s) size(tiny)) ///
				text(3.66 0.2693 "0.2693", place(s) size(tiny)) ///
				text(2.66 0.8972 "0.8972", place(s) size(tiny)) ///
				text(2.66 0.6967 "0.6967", place(s) size(tiny)) ///
				text(2.66 1.0977 "1.0977", place(s) size(tiny)) ///
				text(1.66 0.4965 "0.4965", place(s) size(tiny)) ///
				text(1.66 0.2740 "0.2740", place(s) size(tiny)) ///
				text(1.66 0.7191 "0.7191", place(s) size(tiny)) ///
				text(0.71 -0.1043 "-0.1043", place(s) size(tiny)) ///
				text(0.71 -0.2728 "-0.2728", place(s) size(tiny)) ///
				text(0.71 0.0641 "0.0641", place(s) size(tiny)) ///
				text(6.25 -0.7 "D", tstyle(heading) size(5) place(e)) 

* save graph
graph save figure_llama.gph, replace
graph export figure_llama.png, as(png) replace


* --------------
* Combine
* --------------

resizecombine "figure_gpt4o" "figure_gemini" "figure_claude" "figure_llama", ///
cols(2) ysize(20cm) xsize(30cm) imargin(5 5 5 5)

graph save "Figure5.gph", replace
graph export Figure5.eps, as(eps) replace






















