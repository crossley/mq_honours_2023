from psychopy import gui

test = '''We are seeking healthy volunteers with normal or corrected-to-normal vision and normal hearing to participate in a study that investigates the cognitive mechanisms underlying 
visual and/or auditory processing, human sensorimotor learning, processing of body-related information and how such information modulates perception and action. 

This research is being conducted by Elijah Atienza (Honours Student, telephone (04) 1675 0281, email elijah.atienza@students.mq.edu.au) as being conducted to meet the 
requirements of Bachelor of Psychology (Honours) under the supervision of Matthew Crossley (email matthew.crossley@mq.edu.au) and David Kaplan (email david.kaplan@mq.edu.au)
of the Faculty of Medicine, Health, and Human Sciences. 

If you decide to participate, you will be asked to view and respond to novel visual stimuli, involving sinewave gratings that will be displayed on a computer screen. You may be asked to 
provide button-press responses during the session. The responses you make, and the timing associated with your responses will be collected. The experimental session may take up 
to 30 minutes to complete, and no risks are expected to result from participation. 

You will receive $15 per hour (or pro rata) for your participation. If you are participating for course credit you will receive one and a half credits for each half-hour of face-to-face 
participation and one course credit for each half-hour of online participation.

Any information or personal details (e.g., age, gender) gathered in the course of the study are kept confidential, except as required by law.  No individual will be identified in any 
publication of the results. Access to identifiable data is limited to persons listed on this consent form. Your individual de-identified (anonymised) data obtained through this research may 
be used in future research publications and be made available to journals/reviewers to support publications, as well as in online data repositories, such as the Open Science 
Framework (www.osf.io). At no time will you be identifiable in any published materials because any public information will be provided in such a way that you cannot be identified.

A summary of the results of the data can be made available on request, please give an email address if you would like to receive this.

Participation in this study is voluntary and you are free to withdraw from further participation in the research at any time without having to give a reason and without consequence. 
Macquarie University students who are participating as part of their course requirements will not forfeit their course credits if they choose to withdraw from the research.

By agreeing below, I acknowledge that I have read (or, where appropriate, have had read to me) and understand the information above and any questions I have asked have been 
answered to my satisfaction. I agree to participate in this research, knowing that I can withdraw from further participation in the research at any time without consequence. I have 
been given a copy of this form to keep.

The ethical aspects of this study have been approved by the Macquarie University Human Research Ethics Committee. If you have any complaints or reservations about any ethical 
aspect of your participation in this research, you may contact the Committee through the Director, Research Ethics & Integrity (telephone (02) 9850 7854; email ethics@mq.edu.au). 
Any complaint you make will be treated in confidence and investigated, and you will be informed of the outcome.'''

myDlg = gui.Dlg(title="Ethics and Consent")
myDlg.addText(test)
myDlg.addText('Participant infomation:')
myDlg.addField('Full Name:')
myDlg.addField('Student Email:')
myDlg.addField('Age:')
myDlg.addField('Gender:', choices=['Prefer not to specify', 'Male', 'Female', 'Other'])
ok_data = myDlg.show()
if myDlg.OK:
    print('user consented')
else:
    print('user cancelled')
    core.quit()
