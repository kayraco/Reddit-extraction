import argparse
import json
import requests
from datetime import datetime


def export_posts(subreddit, num_posts, outputfn):
    date = datetime.today().strftime('%Y%m%d')
    outfile = open(str(outputfn + date + '_politics.json'), 'w')

    after = 'null'
    while 0 < num_posts:
        limit = (100 if num_posts >= 100 else num_posts)
        data = requests.get(f'http://api.reddit.com/r/{subreddit}/hot?limit={limit}&after={after}',
                            headers={"User-Agent": "windows:requests (by /u/chiaraobscuro)"})

        content = data.json()
        after = content['data']['after']

        posts = content['data']['children']
        for post in posts:
            json.dump(post, outfile)
            outfile.write('\n')
        num_posts -= 100
    outfile.close()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outfile', help='output filepath')
    parser.add_argument('subreddit', help='subreddit name')
    args = parser.parse_args()
    output_path = args.outfile

    export_posts(args.subreddit, 500, str(output_path))


if __name__ == '__main__':
    main()
