# Welcome to HighTeach contributing guide <!-- omit in toc -->

Thank you for investing your time in contributing to our project! :sparkles:

In this guide you will get an overview of the contribution workflow from opening an issue, creating a PR, reviewing, and merging the PR.


## New contributor guide

To get an overview of the project, read the [README](README.md). Here are some resources to help you get started with open source contributions:

- [Finding ways to contribute to open source on GitHub](https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github)
- [Set up Git](https://docs.github.com/en/get-started/quickstart/set-up-git)
- [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Collaborating with pull requests](https://docs.github.com/en/github/collaborating-with-pull-requests)


## Getting started

### Issues

#### Create a new issue

If you spot a problem with HighTeach, [search if an issue already exists](https://github.com/redhat-beyond/HighTeach/issues). If a related issue doesn't exist, you can [open a new issue](https://github.com/redhat-beyond/HighTeach/issues/new/choose).

#### Solve an issue

Scan through our [existing issues](https://github.com/redhat-beyond/HighTeach/issues) to find one that interests you. As a general rule, we don’t assign issues to anyone. If you find an issue to work on, you are welcome to open a PR with a fix.

### Make Changes

1. Fork the repository.
- Using GitHub Desktop:
  - [Getting started with GitHub Desktop](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/getting-started-with-github-desktop) will guide you through setting up Desktop.
  - Once Desktop is set up, you can use it to [fork the repo](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/cloning-and-forking-repositories-from-github-desktop)!

- Using the command line:
  - [Fork the repo](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo#fork-an-example-repository) so that you can make your changes without affecting the original project until you're ready to merge them.

2. Follow the instructions in the [README.md file](README.md) to set up a working environment.

3. Create a working branch and start with your changes!

### Commit your update

Commit the changes once you are happy with them.
The commit message should explain what changes have been made, and why. 
In addition, they should include a link to the relevant `issue`.

Please use the guide below in order to follow our commit message convention:
* [commit convention](https://cbea.ms/git-commit/#seven-rules)

### Pull Request

When you're finished with the changes, create a pull request, also known as a PR.

- Each PR should include at most 5 `commits`.
- Make sure the PR passes CI checks. Run `pipenv run flake8 --max-line-length 120` and `pipenv run python -m pytest -v` inside your VM before submitting a new PR.
- Before submitting a PR for review, try applying the principle of single responsibility. If this code is doing more than one thing, break it into other PRs.

PR documentation:

- Every PR should have a meaningful and concise title that clearly describes its purpose.
- Every PR should have a meaningful and concise description that provides relevant information on the PR.
- Every PR should be linked to an issue (or issues), to make its purpose clear and increase its visibility (see [Issues](#issues)).
- Assign other contributors as well as maintainers as reviewers on your PR.

PR code review:

- Each pull request requires the approval of at least <ins>2 contributors</ins> and has to be reviewed by the maintainers before merging. 
- Examine the PR carefully, and with respect to what it is supposed to achieve.
- If you want to request changes to specific lines in a file please use the "Start a review" button.
- If you want to request changes, mark your review as "Request changes" - please do not use a generic comment.
- Use polite, respectful and clear language when commenting on or reviewing a PR.
- If your PR recieved a request for changes or a comment, please notify the reviewer about your actions
   (what changes you made, or if you don't think they're necessary - why you think so).

### Your PR is merged!

Congratulations :tada::tada: The HighTeach team thanks you :sparkles:.

Once your PR is merged, your contributions will be publicly visible on the [HighTeach repository](https://github.com/redhat-beyond/HighTeach).