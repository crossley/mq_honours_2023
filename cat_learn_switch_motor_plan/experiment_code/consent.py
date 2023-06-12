from psychopy import gui

test = '''We are seeking healthy volunteers with normal or corrected-to-normal vision and normal hearing to participate in a study that investigates
the cognitive mechanisms underlying visual and/or auditory processing, human sensorimotor learning, processing of body-related information and how
such information modulates perception and action.

This research is being conducted by Dr. Matthew Crossley, Department of Cognitive Science, 9850 2970, matthew.crossley@mq.edu.au.

If you decide to participate, you will be asked to view and respond to simple visual stimuli (e.g., lines that vary in length and orientation). You
will be asked to provide button-press responses during the session. The responses you make and the timing associated with your responses will be
collected. The experimental session may take up to 60 minutes to complete, and no risks are expected to result from participation.

You will receive either course credit or $15 per hour (or pro rata) for your participation. If you are participating for course credit you will receive
one credit for each half-hour of your participation.

Any information or personal details (e.g. age, gender) gathered in the course of the study are kept confidential, except as required by law. No
individual will be identified in any publication of the results. Access to the data is limited to persons directly involved in the research. Your
individual de-identified (anonymised) data obtained through this research may be used in future research publications and be made available to
journals/reviewers to support publications. At no time will you be identifiable in the publication or by the journal/reviewers. Any publication
information will be provided in such a way that you cannot be identified.

A summary of the results of the data can be made available on request, please give an email address if you would like to receive this.

Participation in this study is voluntary and you are free to withdraw from further participation in the research at any time without having to give a
reason and without consequence. Macquarie University students who are participating as part of their course requirements will not forfeit their course
credits if they choose to withdraw from the research.

By agreeing below, I acknowledge that I have read (or, where appropriate, have had read to me) and understand the information above and any questions
I have asked have been answered to my satisfaction. I agree to participate in this research, knowing that I can withdraw from further participation in
the research at any time without consequence. I have been given a copy of this form to keep.

The ethical aspects of this study have been approved by the Macquarie University Human Research Ethics Committee. If you have any complaints or
reservations about any ethical aspect of your participation in this research, you may contact the Committee through the Director, Research Ethics &
Integrity (telephone (02) 9850 7854; email ethics@mq.edu.au). Any complaint you make will be treated in confidence and investigated, and you will be
informed of the outcome.'''

myDlg = gui.Dlg(title="Ethics and Consent")
myDlg.addText(test)
myDlg.addText('Participant info')
myDlg.addField('Name:')
myDlg.addField('Email:')
myDlg.addField('Age:')
myDlg.addField('Gender:', choices=['Prefer not to specify', 'Male', 'Female', 'Other'])
ok_data = myDlg.show()
if myDlg.OK:
    print('user consented')
else:
    print('user cancelled')
    core.quit()
