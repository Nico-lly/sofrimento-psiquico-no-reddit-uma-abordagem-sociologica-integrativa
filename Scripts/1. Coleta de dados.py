import praw
import time
import pandas as pd

# Authenticate with the Reddit API
reddit = praw.Reddit(client_id='insert client id',
                     client_secret='insert client secret',
                     user_agent='insert user agent',
                     username='insert user name',
                     password= "insert password")


# Set the subreddit name and the maximum number of submissions to fetch
subreddit_name = 'Desabafos'
max_submissions = 1000

# Fetch the subreddit object from the Reddit API
subreddit = reddit.subreddit(subreddit_name)

# Initialize a list to hold the fetched submissions
submissions = []

# Fetch submissions using pagination until we reach the maximum number or run out of submissions
last_submission_name = None

cont = 0
while len(submissions) < max_submissions:
    cont = cont + 1
    
    # Fetch up to 100 submissions, starting from the last submission time
    fetched_submissions = subreddit.rising(limit=100, params={'after': last_submission_name})
    print(f'sub nº: {cont}')
    
    # Iterate over the fetched submissions
    for submission in fetched_submissions:
        submission_dict = {}
        # Convert the submission object to a dictionary
        submission_dict['title'] = submission.title
        submission_dict['selftext'] = submission.selftext
        submission_dict['id'] = submission.name
        submission_dict['created'] = submission.created
        submission_dict['up'] = submission.ups
        submission_dict['coments'] = submission.num_comments
        
        # Add the dictionary to the list of submissions
        submissions.append(submission_dict)
    
        # Update the last_submission_time to the created_utc of the next submission
        last_submission_name = submission.name
        print(last_submission_name)
        
    # If we've fetched the maximum number of submissions, break out of the loop
    if len(submissions) > max_submissions:
        break
    
    
    time.sleep(3)
    

#Creating a dataframe with all the dictionaries in the list
df = pd.DataFrame()
for dictionary in submissions:
    df = df.append(pd.Series(dictionary), ignore_index=True)

#Generating a csv with the dataframe data
df.to_csv('submissions_rising_2023_04_06.csv', encoding = 'utf8', sep = ',', index=False)

ids_unicos = []
for submission in submissions:
    _id = submission['id']
    if _id not in ids_unicos:
        ids_unicos.append(_id)