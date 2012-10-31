Feature: Polls
Scenario: Vote in the browser
  When I visit url "/admin"
   And I login as "<username>" with password "test"
   And I load value "polls.models.Poll.objects.get(id=1)" in "self.poll"
   And I load value "polls.models.Choice.objects.get(poll=self.poll,choice_text='<choice_text>')" in "self.choice"
   And I visit url "/vote/1"
   And I fill in field "choice" with value "eval:self.choice.id"
   And I submit the form
  Then I'm redirected to url "/total_votes/1/"
   And I see the text "Total Votes <total_votes>"
   And I see the text "<choice_text> <votes_percent>"

  | username | choice_text | total_votes | votes_percent |
  | user01   | Vi          | 1           | 100%          |
  | user02   | Gedit       | 2           | 50%           |
  | user03   | PyCharm     | 3           | 33%           |
  | user04   | PyCharm     | 4           | 50%           |
  | user05   | Eclipse     | 5           | 20%           |
  | user06   | Vi          | 6           | 33%           |
  | user07   | WingIDE     | 7           | 14%           |

Scenario: Redirect to login
  When I visit url "/vote/1"
  Then I'm redirected to url "/admin/?next=/vote/1/"

Scenario: Page not found
  When I visit url "/admin"
   And I login as "user01" with password "test"
   And I visit url "/vote/2"
  Then I see the text "Page not found"

Scenario: Add new poll
  When I visit url "/admin"
   And I login as "user01" with password "test"
   And I visit url "/admin/polls/poll/add"
   And I fill in field "question" with value "Choose your favorite videogame character"
   And I submit the form
   Then I see the text "was added successfully."

Scenario: Add new choices
  When I visit url "/admin"
   And I login as "user01" with password "test"
   And I visit url "/admin/polls/choice/add"
   And I fill in fields "poll,choice_text" with values "Choose your favorite videogame character,<choice_text>"
   And I submit the form
   Then I see the text "was added successfully."
    And I see an object "polls.models.Choice" with values "{'choice_text':'<choice_text>'}"

    | choice_text |
    | Mario       |
    | Solid Snake |
    | Link        |
    | Pac-man     |
    | Cloud (FF7  |
