__author__ = 'bzhang'

import utility
import time
import logging


def generate_log(x, y, elapse):
    logs.append('the num of participants is {0}'.format(x))
    logs.append('the num of messages {0}'.format(y))
    logs.append('the elapse time is {0}'.format(elapse))


course_id = '_3_1'
rawText = 'hello'

logs = []
rest = utility.Utility()
rest.login()
rest.token()
course_memberships = rest.get_course_memberships(course_id)['results']
json_body = {'participantIds': [course_memberships[0].get('userId'), course_memberships[1].get('userId')],
             'canBeRepliedTo': True,
             'isBroadcast': False,
             'messages': [{"body": {'rawText': rawText, 'displayText': ''}}]}
for c in range(1, 100):
    conversation = rest.create_course_conversation(course_id, json_body)
    logging.error(conversation.get('id'))
    for i in range(2, 100, 50):
        new_participant_ids = []
        for j in range(i, i + 10):
            if j >= len(course_memberships):
                continue
            else:
                new_participant_ids.append(course_memberships[j].get('userId'))
        conversation = rest.add_participants_to_course_conversation(course_id, conversation.get('id'), new_participant_ids)
        for k in range(0, 1):
            start = time.time()
            rest.send_message_in_conversation(course_id, conversation.get('id'))
            end = time.time()
            generate_log(i + 1, k, end - start)
    logging.error(c)
    for tmp in logs:
        logging.error(tmp)



