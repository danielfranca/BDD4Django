Feature: Polls
Scenario: Vote in a choice
 Given a poll "What's the best Python IDE/Editor?" with choices "WingIDE,PyCharm,Vi,Gedit,Eclipse,Aptana"
  When I load value "polls.models.Poll.objects.get(id=1)" in "self.poll"
   And I load value "polls.models.Choice.objects.get(poll=self.poll,choice_text='<choice_text>')" in "self.choice"
   And I call view "vote,args=(1,)" with post data "{'choice':self.choice.id}" as user "<username>" with password "test"
  Then I'm redirected to url "/total_votes/1/"
   And I see the text "<td>Total Votes</td><td><total_votes></td>" in template
   And I see the text "<td><choice_text></td><td><votes_percent></td>" in template

  | username | choice_text | total_votes | votes_percent |
  | user01   | Vi          | 1           | 100%          |
  | user02   | Gedit       | 2           | 50%           |
  | user03   | PyCharm     | 3           | 33%           |
  | user04   | PyCharm     | 4           | 50%           |
  | user01   | PyCharm     | 4           | 50%           |
  | user05   | Eclipse     | 5           | 20%           |
  | user01   | Eclipse     | 5           | 20%           |
  | user06   | Vi          | 6           | 33%           |
  | user07   | WingIDE     | 7           | 14%           |
