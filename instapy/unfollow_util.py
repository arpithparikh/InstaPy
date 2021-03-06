"""Module which handles the follow features like unfollowing and following"""
import json

from .time_util import sleep


def unfollow(browser, username, amount, dont_include):
  """unfollows the given amount of users"""
  unfollowNum = 0

  browser.get('https://www.instagram.com/' + username)

  following_link_div = browser.find_elements_by_class_name('_218yx')[2]
  following_link = following_link_div.find_element_by_tag_name('a')
  following_link.click()

  sleep(2)

  person_list_div = browser.find_element_by_class_name('_4gt3b')
  person_list = person_list_div.find_elements_by_class_name('_cx1ua')

  person_list = [x.find_element_by_class_name('_gzjax').text for x in person_list]

  follow_div = browser.find_element_by_class_name('_4gt3b')
  follow_buttons = follow_div.find_elements_by_tag_name('button')

  for button, person in zip(follow_buttons[:amount], person_list[:amount]):
    if person not in dont_include:
      unfollowNum += 1
      button.click()
      print('--> Now unfollowing: {}'.format(person.encode('utf-8')))
      sleep(15)

  return unfollowNum

def follow_user(browser, user_name, follow_restrict):
  """Follows the user of the currently opened image"""
  follow_button = browser.find_element_by_xpath("//article/header/span/button")
  sleep(2)

  if follow_button.text == 'Follow':
    follow_button.click()
    print('--> Now following')

    follow_restrict[user_name] = follow_restrict.get(user_name, 0) + 1
    sleep(3)
    return 1

  else:
    print('--> Already following')
    sleep(1)
    return 0

def dump_follow_restriction(followRes):
  """Dumps the given dictionary to a file using the json format"""
  with open('./logs/followRestriction.json', 'w') as followResFile:
    json.dump(followRes, followResFile)

def load_follow_restriction():
  """Loads the saved """
  with open('./logs/followRestriction.json') as followResFile:
    return json.load(followResFile)
