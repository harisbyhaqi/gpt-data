import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

ati = pd.read_excel("collected_data.xlsx") #Declare the Pands File Object


"""
TABLE I - DISTRIBUTION OF STUDENTS IN DIFFERENT
          PROGRAMS AND USE OF CHATGPT
          
Note: Data was collected using Matplotlib however table was custom
made using Microsoft Word
"""
#Get the uses from the "Use GPT" column in excel and convert to list
uses = ati['Used GPT'].tolist()
#Get the programs from the 'Program' column in excel and convert to list
programs = ati['Program'].tolist()
#Create the uses response dictionary. Each value is the program and the key is a list where: [Used GPT before, Haven't used GPT before]
uses_response = {}
#Define the main programs. The majority of survey-responders are part of the main programs
#defined in this list
main_programs = ["computer science", "business technology management",
                 "business management", "engineering", "life science",
                 "accounting and finance"]


#Iterate over the programs list from excel
for i, program in enumerate(programs):
    program = program.lower().strip() #Lowercase it and strip it of whitespaces in beginning and end
    if program not in main_programs: #If the current program is not classified as a "main program" defined above
        program = "Other" #Set the program to "Other"
    if program not in uses_response.keys(): #If the program is not already in the dictionary
        uses_response[program] = [0,0] #Set the value of that program key to [0,0]. The reasoning for each element is mentioned above
    if uses[i] == "Yes": #If the "Used GPT" response for the current person is "YeS", increment the first element
        uses_response[program][0] += 1
    elif uses[i] == "No": #Else if the "Used GPT" response for the current person is "No", increment the second element.
        uses_response[program][1] += 1

#UNCOMMENT THE LINEs BELOW IF YOU WANT TO SEE THE RESULTS FOR TABLE I.
for program, uses in uses_response.items():
    print(f"{program}:")
    print(f"Yes: {uses[0]} No: {uses[1]}\n")

"""
FIGURE 2 - BAR GRAPH DISTRIBUTION OF DIFFERENT PROGRAMS AND 
           THEIR REASONING FOR USING CHATGPT IN GENERAL
"""
#Clear the plot
plt.clf()

"""
Set plot for dark background for the google slides. UNCOMMENT the line to see the results of it
"""
plt.style.use('dark_background')
# Create the progam and their reasons to use GPT and sort it into a dictioanry
programs = {}
#Get the reasons from the 'Reason' column in excel and convert it to a list using the builtin method of a DataFrame object
reasons = ati['Reason'].tolist()

#Store the "unique" reasons in a set. Reason for this is because when making the 
#survey, we allowed survery-responses to pick multiple options for this question
#This means that per student there can be multiple reasons, therefore we have to
#go through all those reasons and put them into a set, which allows for unique objects
unique_reasons = set()
#Define the main programs. The majority of survey-responders are part of the main programs
#defined in this list
main_programs = ["computer science", "business technology management",
                 "business management", "engineering", "life science",
                 "accounting and finance"]

for i, program in enumerate(ati['Program'].tolist()):
    program = program.lower().strip() #set the program name to lowercase to ignore case sensitivity and remove whitespaces from beginning and end
    if program not in main_programs: #If the program is not defined as the one in the main programs, it's classified as "other"
        program = "Other"
    if program not in programs.keys(): #If the program is not in programs dictionary, add it
        programs[program] = {}
    else:
        currReason = reasons[i] #Get the reason(s) correpsonding with the program the current student is in.
        if type(currReason) == str and currReason != "li": #If the current reason is a string, and for some apparent reason, the word "li" was apart of some reasons
                                                       #to counter this, we jus checked if the current response is not "li". Only reason we checked if it was a string
                                                       # was because if the person didn't respond with anything, it sets this field
                                                        #to "nan" which is declared as a float in python [even tho it's Not A Number?]

            for cr in currReason.split(','): #Iterate over the reasons.split(','). This makes it so that if the current person entered mutliple reasons on the 
                                             #survey, it put them in this format: "Reason 1, Reason 2, ...". To counter this, .split(',') converts all the reasons
                                             #into a list and iterates over them. If there are no ',' in the string, it just returns a list of the original string

                cr = cr.strip() #Strip the whitespaces in the beginning and end of the list
                unique_reasons.add(cr) #Add the current reason to the unique reasons set as mentioned above
                if cr not in programs[program].keys(): #If the current reason is not in the programs dictionarys corresponding to the current program, set the "count" value to 
                    programs[program][cr] = 1
                else: #If it is, we increment it by 1
                    programs[program][cr] += 1


##Create a pandas DataFrame object and plot it into a stacked bar graph
reason_program = pd.DataFrame(programs)
reason_program.plot(kind='bar', stacked=True)

print(programs)
#Bar graph properties. Set the title, size, and x-axis labels with a slight rotation

#Make the first letter of each program capitalized, and set this as the label
labels = [program[0].upper() + program[1:] for program in reason_program.keys()] 

#Create the plot legend using the labels variable and set it's location to "best"
plt.legend(labels, loc="best")
#Set the ticks on the x axis to increment by 1
plt.xticks(range(0,len(unique_reasons)), unique_reasons, rotation=70)
#Set the plot title to this
plt.title('Reason for use of ChatGPT by students in different program')
#Change the plot size of 1000 x 750 pixels (reasons is because of the DPI)
plt.gcf().set_size_inches(10, 7.5) 
#Add a margin of 0.25 inches to the bottom of the graph image
plt.gcf().subplots_adjust(bottom=0.25)
#SAVE THE PLOT WITH CUSTOM DPI with transparent background (for the presentation)
plt.savefig("reason_program.png", dpi = 100, transparent = True)

"""
FIGURE 3 - HOW MANY PEOPLE THINK IT HAS AN IMPACT ON EDUCATION
"""
###Create the dictionary of responses. Each key is the response type
###and each value corresponds to the amount of people saying that response

#CLEAR THE PLOT
plt.clf()

#Declare the valid responses CONSTANT
VALID_RESPONES = ["Yes", "No", "Maybe"]

#Create a dictionary of each response from the 'Impact' column form the excel check
responses = ati['Impact'].value_counts()
#Create an empty dictionary of the responses
response_dict = {}
#Iterate over the VALID responses const and set the responses_dict dictionary to the value from the 'Impact' column
for response in VALID_RESPONES:
    response_dict[response] = responses[response]

###DECLARING VARIABLES

#Declare the values of each response
values = response_dict.values()
#Declare the labels of each response, which are the keys in the dictionary
label = response_dict.keys()
#Create the colors matching each response. Green means Yes, orange maybe, red no
colors = ["#228B22", "#FF0000", "#FFA500"]
#Using f-string formatting and a list comprehension, reassign every label to the label + responses / total responses for that value
label = [f"{list(label)[i]} ({round(list(values)[i]/ sum(values) * 100,2)}%)" for i in range(len(values))]

## CREATING THE PIE CHART
"""
Set plot for dark background for the google slides. UNCOMMENT the line to see the results of it
"""
plt.style.use('dark_background')

#Create a pie chart in matplotlib with the corresponding values, labels and colors
plt.pie(values, labels = label, colors = colors)
#Set the title of the plot to that
plt.title("Perceived Impact of ChatGPT on Academia by students aged 18-24")
#Add a legend to the pie chart with the corresponding labels. Set the location of the legend to "best" which is usually upper-right by default
plt.legend(labels=label, loc="best")



#Save the figure as 'impact.png' in the current directory with transparent background (for the presentation)

plt.savefig("impact.png", transparent=True)


"""
FIGURE 4 - HOW MANY PERCENTAGE OF STUDENTS WHO THINK
           CHATGPT MAKES AN IMPACT IN ACADEMIA ARE COMP SCI KIDS
           COMPARED TO OTHER PROGRAMS
"""

#CLEAR THE PLOT
plt.clf()

"""
Set plot for dark background for the google slides. UNCOMMENT the line to see the results of it
"""
plt.style.use('dark_background')

#DECLARE DICTIONARY TO HOLD VALUES
#The value of each key follows: [number of students who said yes, total students in this program]
program_impacts = \
{"computer science": [0,0],
 "business technology management":[0,0],
 "engineering" :[0,0],
 "accounting and finance" :[0,0],
 "business management" :[0,0],
 "life science": [0,0],
 "Other" :[0,0]}

# Create the zip object of program to impact.
# Each zip objects contains a tuple of the program
# and what they said about impact of ChatGPT
program_to_impact_relation = zip(ati['Program'].tolist(), ati['Impact'].tolist())
for program, percieved_impact in program_to_impact_relation: #Iterate over the zipped object
    program = program.lower().strip()        #make it all lowecase and get rid of whitespaces at the beginning and end of the string
    if program not in program_impacts.keys():#If the current program is not in the keys, aka classified as "Other"
        program = "Other"                    #Sets program to "Other"
    if percieved_impact == "Yes":            #If they think that ChatGPT does make an impact in academia
        program_impacts[program][0] += 1     #Add 1 to the first element of the list. As mentioneed above, the first element is the # of students who said yes
    program_impacts[program][1] += 1         #Increment the second element of the list. The second element is the total number of students


#Graph variables

#Make the first letter of each program capitalized, and set this as the label using a list comprehension
labels = [program[0].upper() + program[1:] for program in reason_program.keys()] 
#Create values_1, which is the amount of people that said 'Yes' per program
values_1 = [value[0] for value in program_impacts.values()]
#Create values_2 which is the total number of students in that program
values_2 = [value[1] for value in program_impacts.values()]
#Instantiate the total number of programs from the labels list
x = range(len(labels))
#Set the width of each bar to 0.35 inches
bar_width = 0.35

#Graph the dictionary in matplotlib
#Create the figure and axis objects 
fig, ax = plt.subplots()
#Create a bar on the axis based on the bar width, bar label, bar value, and bar location
ax.bar(x, values_1, width=bar_width, label="Number of students who said yes")
#Create a 2nd bar on the axis, which is is in charge of graphing the total number of students.
ax.bar([i + bar_width for i in x], values_2, width=bar_width, label="Total number of students")
#Create x-axis ticks in the graph that increment by the bar_widh / 2
ax.set_xticks([i + bar_width / 2 for i in x])
#Set the x-axis labels to the labels defined above
ax.set_xticklabels(labels)

#Modify the bar graph attributes in matplotlib


#Set the x axis labels to have a rotaton of 45 degrees to the right
plt.xticks(rotation=45, ha='right')
#Create a legend of the plot and assign it to the best location possible
plt.legend(loc = "best")
#Set the title to the plot of that
plt.title("Number of students who said ChatGPT can make an impact in acamdemia vs total students in different programs")
#Change size of the bar graph to 1000 x 750 pixels
plt.gcf().set_size_inches(10, 7.5) 
#Add a whitespace gap of 0.30 inches at the bottom to prevent the x-axis text from cutting off
plt.gcf().subplots_adjust(bottom=0.30)

#Save the plot as "yes_programs.png" with a DPI of 100
#This DPI means that the resolution as mentioned above
#is going to be x * DPI, y * DPI
# x = 10 * 100 = 1000, y = 7.5 * 100 = 750

#Save figure with transparent background (for the presentation)
plt.savefig("yes_programs.png", dpi = 100, transparent=True)
