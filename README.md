# CohortSignUpFirstOrder
Two Python applications: building a cohort from simulated data and counting venues in cities using Foursquare API. A report in pdf is included in "exercise-1"
<ul>
	<li> Building a cohort of Signup's vs first order's. <b>Folder: "exercise-1"</b>. </li>
<li> The number of laundry, hairdressing and fitness stores per 100k habitants. <b>Folder: "exercise-2"</b>. </li>
</ul>

## Building a cohort of Signup's vs first order's
The folder <i>exercise-1</i> contains the Python code <b> library_simulate_data.py </b> to generate a population of user ID's and signup timestamps:
<table id="pnptab">
		<tr>
			<th> User ID </th>
			<th> sign_up_timestamp </th>			
		</tr>
		<tr>
			<td> 0102V </td>		
			<td> 2018/04/02 </td>
		</tr>
		<tr>
			<td> ... </td>		
			<td> ... </td>
		</tr>
</table>		
and another random population with coherent orders of the users population:
<table id="pnptab">
		<tr>
			<th> User ID </th>
			<th> order_timestamp </th>			
		</tr>
		<tr>
			<td> 2313Q </td>		
			<td> 2019/01/13 </td>
		</tr>
		<tr>
			<td> ... </td>		
			<td> ... </td>
		</tr>
</table>		
The order timestamps are generated in a period of 5 weeks after the login date for each user.

### The cohort
The goal is to construct from the former two tables a cohort counting: from the users that signed up in week N, the users that made the first order in week N + k. Something like this:
<table id="pnptab">
		<tr>
			<th> Week </th>
			<th> number </th>						
			<th> N+0 [%] </th>			
			<th> N+1 [%]</th>						
			<th> N+2 [%]</th>						
			<th> ... </th>			
		</tr>
		<tr>
			<th> Week 1</th>
			<th> 58 </th>						
			<th> 45 </th>			
			<th> 25 </th>						
			<th> 7 </th>						
			<th> ... </th>			
		</tr>
		<tr>
			<th> Week 2</th>
			<th> 12 </th>						
			<th> 34 </th>			
			<th> 23 </th>						
			<th> 9 </th>						
			<th> ... </th>	
		</tr>
		<tr>
			<th>...</th>
			<th> ...</th>						
			<th> ... </th>			
			<th>... </th>						
			<th>...</th>						
			<th>... </th>	
		</tr>
	
</table>		
</p>
The python script  <b> main_cohort_signup.py </b> contains the code to generate the cohort table from two pandas dataframes.

## The number of laundry, hairdressing and fitness stores per 100k habitants
In this simple script I use Foursquare API requests to obtain the number of laundry, hairdressing and fitness stores per 100k habitants in two cities of France and Germany. It consists on two scripts contained in folder <i>exercise-2</i>:  <b> gymsLaundryBeaty_foursquareAPI.py.py </b> and  <b> tableComparison.py </b>. The output table from the latter script is in latex format.
