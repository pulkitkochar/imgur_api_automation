Feature: End to end journey

  Scenario: Up grad Assignment
    Given I am logged in as pulkitko1991
    When I get account details of current logged in user
    Then I verify the account details and user id should be 136476219
    When I update username as pulkitko1991upgrad
    And I get account details of current logged in user
    Then I verify the account details and user id should be 136476219
    When I update username as pulkitko1991
    And I get account details of current logged in user
    Then I verify the account details and user id should be 136476219
    Given Images are already uploaded
    When I create a new album called assignment
    And I add uploaded images to assignment album
    And I made assignment album public
    Then I verify details of assignment album and it should not be my favourite
    When I mark assignment album as my favourite
    Then I verify details of assignment album and it should be my favourite
    When I logout and login as pulkitkochar1991
    And I comment Thanks for sharing on assignment album
    When I logout and login as pulkitko1991
    And I access the comments on assignment album and up vote them
    Then I verify all the comments has upvote on assignment album
    When I reply Thanks to the comments on assignment album
    When I delete the assignment album
    Then I should not see assignment album
