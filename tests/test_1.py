import json
import pytest
from unittest.mock import patch


# Mock SQS queues
@pytest.fixture(scope='function')
def queue_url_mock(sqs_client):
    '''create mock queues for use in the p1,2, and 3 tests'''
    queue_urls = {
        '1': sqs_client.create_queue(QueueName='P1Queue')['QueueUrl'],
        '2': sqs_client.create_queue(QueueName='P2Queue')['QueueUrl'],
        '3': sqs_client.create_queue(QueueName='P3Queue')['QueueUrl']
    }
    return queue_urls

def test_submit_bug_report_valid_p1(client, sqs_client, queue_url_mock):
    '''test to check the queues are functional in sending messages'''
    queue_urls = queue_url_mock

    with patch('main.queue_urls', queue_urls):
        response = client.post('/submit_bug_report', data={
            'title': 'Teams Bug Test',
            'description': 'sending a teams message',
            'priority': '1'
        })
        
    messages = sqs_client.receive_message(QueueUrl=queue_urls['1'])
 
    expected_message = {'title': 'Teams Bug Test', 'description': 'sending a teams message'}
    assert json.loads(messages['Messages'][0]['Body']) == expected_message


def test_submit_bug_report_invalid_priority(client, sqs_client):
    '''test to check if the queues throw an error with an invalid queue priority number'''
    response = client.post('/submit_bug_report', data={
        'title': 'Teams Bug Test',
        'description': 'Sending a teams message',
        'priority': '5'  
    })
    
    assert response.status_code == 400
    assert b'{"error":"Invalid priority"}\n' in response.data


def test_health_check(client):
    '''test to check if the health check is functionsl'''
    response = client.get('/health')

    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

