from main import *
import json
import sys

def load_mock_data(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)

    printProgressBar(0, len(data), 
        prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, user_data in enumerate(data):
        company = Company.query.filter_by(name=user_data['company']).first()
        if company is None:
            company = Company(name=user_data['company'])
            db.session.add(company)
        # Email should be unique.
        if User.query.filter_by(email=user_data['email']).first() is not None:
            continue
        user = User(
            first_name=user_data['name'].split()[0],
            last_name=user_data['name'].split()[1],
            email=user_data['email'],
            phone=user_data['phone'],
        )
        company.people.append(user)
        for user_skill_data in user_data['skills']:
            skill = Skill.query \
                .filter_by(name=user_skill_data['skill']).first()
            if skill is None:
                skill = Skill(name=user_skill_data['skill'])
                db.session.add(skill)
            
            user_skill = UserSkill(user=user, skill=skill, 
                rating=user_skill_data['rating'])
            db.session.add(user_skill)
        printProgressBar(i + 1, len(data), 
            prefix = 'Progress:', suffix = 'Complete', length = 50)

    db.session.commit()

# Print iterations progress https://stackoverflow.com/questions/3173320/
def printProgressBar (
    iteration, total, 
    prefix = '', suffix = '', decimals = 1, length = 100, 
    fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}") \
        .format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    file_name = "mock_userdata.json"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    load_mock_data(file_name)
