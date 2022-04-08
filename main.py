from flask import Flask, render_template, request, redirect
from questions import Questions

app = Flask(__name__, template_folder='templates')

"""
    We gonna create the lists of questions that are below
"""

selected_data = [[0, 'a']]
answers = [[0, 'b'], [1, 'a'], [2, 'e'], [3, 'd'], [4, 'c'], [5, 'b'], [6, 'a'], [7, 'a'],
           [8, 'a'], [9, 'b'], [10, 'c'], [11, 'a'], [12, 'b'], [13, 'b'], [14, 'a'], [15, 'a'],
           [16, 'b'], [17, 'c'], [18, 'c'], [19, 'b'], [20, 'b'], [21, 'b'], [22, 'a'], [23, 'c'], [24, 'c'], [25, 'a'],
           [26, 'a'], [27, 'c'], [28, 'a'], [29, 'b'], [30, 'b'],
           # These Below values are as per pdf document but not in word file
           # [31, 'b'], [32, 'a'], [33, 'a'],
           # [34, 'b'], [35, 'c'], [36, 'b'], [37, 'a'], [38, 'e'], [39, 'd'], [40, 'c'], [41, 'b'],
           # [42, 'a'], [43, 'a'], [44, 'd'], [45, 'b'], [46, 'c'],[47, 'a'], [48, 'b'], [50, 'b'],
           # [51, 'a'], [52, 'a'], [53, 'b'], [54, 'c'], [55, 'b'], [56, 'a'], [56, 'e'], [57, 'd'],
           # [58, 'c'], [59, 'b'], [60, 'a'], [61, 'a'],
           ]

# for i in Questions:
#     print(i[1]['a'])

"""
    The route below is Specific interfaces screen to start survey
"""

page = 0
last = 30

"""
    This function below checks the data before adding to the list if the record in the list is already exsist
"""


def checkbeforeappending(temp):
    if temp[0] is None:
        return False

    for i in selected_data:
        if temp[0] == i[0]:
            return False
    return True


"""
    This Function below checks the answers while having comparison to the selected one
"""

earned_grades = 0


def checkanswers():
    global earned_grades
    for i in range(0, 30):
        if selected_data[i][1] == answers[i][1]:
            earned_grades = earned_grades + 1

    print('you have earned grades', earned_grades)
    print(answers)
    print(selected_data)


@app.route('/')
def startsurvey():
    return render_template('startsurvey.html')


@app.route('/higherlevelstudy', methods=['POST', 'GET'])
def higherlevelstudy():
    if request.method == 'POST':
        check_if_one_agree = request.form.get('optradio')
        print(check_if_one_agree)
        return redirect('/questions')
    return render_template('higherlevelstudy.html')


@app.route('/doyouagree', methods=['POST', 'GET'])
def doyouagree():
    if request.method == 'POST':
        check_if_one_agree = request.form.get('optradio')
        if check_if_one_agree == 'Yes':
            return redirect('/higherlevelstudy')
        return redirect('/')
    return render_template('doyouagree.html')


@app.route('/questions', methods=['POST', 'GET'])
def questions():
    page = request.args.get('page')  # We will get the number of page at which we are from URL
    get_question_value = request.args.get('value')  # We will get the Selected Value from User

    temp = [page, get_question_value]  # This is used to Temporary store the value to pass the function and check
    # weather the value exist

    chck = checkbeforeappending(temp)  # This will pass the values to function and check weather the values exist or not

    if chck:  # if the function returns true means values does not exist and append the selected value to the function
        selected_data.append(temp)

    if page == '30':  # This will make comparison when we are at last page and return us the compiled result
        checkanswers()
        return render_template('complete.html', earned_grades=earned_grades)

    if not str(page).isnumeric():  # For the very first it will check the value of page and assign int value to that
        page = 0

    if page == 0:
        forwarded_data = [Questions[page]]
        number_of_choice = len(forwarded_data[0][1])
        prev = '#'
        next = 'page=' + str(page + 1)

        return render_template('questions.html', question_no=page, question=forwarded_data,
                               number_of_choice=number_of_choice,
                               prev=prev, nex=next)

    if page == last:
        forwarded_data = [Questions[page]]
        number_of_choice = len(forwarded_data[0][1])
        prev = 'page=' + str(page - 1)
        next = '#'

        return render_template('questions.html', question_no=page, question=forwarded_data,
                               number_of_choice=number_of_choice,
                               prev=prev, nex=next)

    prev = "page=" + str(int(page) - 1)
    next = "page=" + str(int(page) + 1)
    forwarded_data = [Questions[int(page)]]
    number_of_choice = len(forwarded_data[0][1])

    return render_template('questions.html', question_no=int(page), question=forwarded_data, prev=prev,
                           nex=next, number_of_choice=number_of_choice)


if __name__ == '__main__':
    app.run(debug=True)
