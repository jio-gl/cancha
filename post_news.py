
import time, json
import html.entities
table_html = {k: '&{};'.format(v) for k, v in html.entities.codepoint2name.items()}
import pathlib

dir_path = str(pathlib.Path.cwd()) + '/'


from calciomercato import getLatest, filterLatest
from api_completion import transformNews
from configuration import all_prompts
from blogger import bloggerPost
from twitter_bot import twit_payload

blog = 'cancha24'
prompts = all_prompts[blog]


def alreadyPublished(article):
    retVal = False
    try:
        open(dir_path + blog + '/' + article['item'], 'r')
        retVal = True
    except:
        retVal = False
    return retVal

def savePublished(article):
    open(dir_path + blog + '/' + article['item'], 'w').write( json.dumps(article) )

def postNews(blog):

    news = getLatest(debug=False)
    # filter by some keywords
    news = filterLatest(news)
    #print(news)

    for article in news[:1]:

        # 1. check if already published
        if alreadyPublished(article):
            print('INFO: already published article -> ' + article['item'])
            continue
        print ('INFO: ###1. check if already published')
        #print(article)

        # 2. transform with AI
        print('INFO: ###2. transform with AI')
        try:
            article['target_title'] = transformNews(article['title'], prompt=prompts['title'])
            time.sleep(2)
            print('sleeping 2 seconds before next AI transform ...')
            article['target_body'] = transformNews(article['body'], prompt=prompts['body'])
        except:
            print('ERROR: error transforming data with AI, possibly text too long.')
            continue 

        # 3. organize source and image and HTML
        print('INFO: ###3. organize source and image and HTML')
        title = article['target_title']
        if title.startswith("'"):
            title = title[1:]
        if title.endswith("'") and title.count("'")%2 == 1:
            title = title[:-1]
        html_title = title.translate(table_html)
        html_body = ''
        if 'image' in article:
            html_body += '<div style="text-align: center;">'
            html_body += '<img src="%s"></img><br/>\n' % article['image']
            html_body += '</div>'
        # body
        html_body += '<div style="text-align: justify;">'
        html_body += article['target_body'].translate(table_html)
        html_body += '</div>'
        html_body += '\n\n<br/><br/><small><a href="%s">Fuente</a></small>\n' % article['item_url']

        # 4. publish
        print('INFO: ###4. publish')
        blog_post_url = bloggerPost(html_title, html_body)
        #break
        # https://www.mattcrampton.com/blog/step_by_step_tutorial_to_post_to_twitter_using_python/

        # 5. saving published
        print('INFO: ###5. saving published')
        savePublished( article )

        # 6. posting twit
        print('INFO: ###6. posting twit')
        twit_payload(title, blog_post_url, article['image'] )

        # https://github.com/raghur/easyblogger
        time.sleep(2.0)
        print('INFO: sleeping 5 seconds per published news article ...')
        pass


if __name__ == '__main__':
    postNews(blog)

    