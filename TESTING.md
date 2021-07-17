# Testing
## Table of Contents
<details>
  <summary>Click to expand table of contents</summary>

1. [User Stories Testing](#user-stories-testing)
2. [Code Validation](#code-validation)
3. [Functionality Testing](#functionality-testing)
4. [Encountered Issues](#encountered-issues)
5. [Web Accessibility](#web-accessibility)
6. [Performance Testing](#performance-testing)
</details>

# User Stories Testing


# Code Validation

- The website was validated by the [W3C Markup Validation Service](https://validator.w3.org/) to ensure there were no syntax errors or issues. 
- [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) was used to validate CSS code.
- [JSHint](https://jshint.com/) was used for JavaScript code validation was used for validation of JavaScript.

## [W3C Markup Validation Service](https://validator.w3.org/) - Markup Validation

### Home Page
- There are no errors
- There is one warning

    <h2 align="center"><img src="readme/images/html_valid_home.jpg" alt="HTML Validation - home page" target="_blank" width="60%" height="60%"></h2>

### About Us Page
- There are no errors
- There is one warning

    <h2 align="center"><img src="readme/images/html_valid_about.jpg" alt="HTML Validation - About us page" target="_blank" width="60%" height="60%"></h2>

### Register Page
- There are no errors
- There is one warning

    <h2 align="center"><img src="readme/images/html_valid_register.jpg" alt="HTML Validation - Register page" target="_blank" width="60%" height="60%"></h2>

### Log in Page
- There are no errors
- There is one warning

    <h2 align="center"><img src="readme/images/html_valid_login.jpg" alt="HTML Validation - Login page" target="_blank" width="60%" height="60%"></h2>

## [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) - CSS Validation

- There are no errors.
- There are several warnings about the vendor prefixes which can be ignored.

    <h2 align="center"><img src="readme/images/css_validation.jpg" alt="CSS Validation" target="_blank" width="60%" height="60%"></h2>

## [JSHint](https://jshint.com/) - JavaScript Validation

### script.js
- There are no errors
- There is one warning showing for a missing semicolon which doesn't make sense since the semicolon is added (line 27)

<h2 align="center"><img src="readme/images/script.jpg" alt="JS validation for script.js file" target="_blank" width="75%" height="75%"></h2>

### jquery.js

- There are no errors
- There is one warning showing for a missing semicolon which doesn't make sense since the semicolon is added (line 5)

<h2 align="center"><img src="readme/images/jquery.jpg" alt="JS validation for jquery.js file" target="_blank" width="75%" height="75%"></h2>

## [PEP8 Online](http://pep8online.com/) - Python PEP8 Compliant

- The website's Python code was checked for PEP8 compliance and returned no errors:

<h2 align="center"><img src="readme/images/pep8.jpg" alt="JS validation for jquery.js file" target="_blank" width="75%" height="75%"></h2>

# Functionality Testing 

Comprehensive testing was executed. Further elaborated in more details below:


## Device Testing

- The website was physically tested on the following devices with different screen sizes:
  - iPhone 7 (Safari & Google Chrome)
  - iPhone 8 (Safari & Google Chrome)
  - iPhone 11 (Safari & Google Chrome)
  - Samsung GTI9505 Galaxy S4 (Chrome for Android)
  - Samsung Galaxy 9 (Chrome for Android & Samsung Internet)
  - Samsung Galaxy S20 (Chrome for Android & Samsung Internet)
  - Nokia Lumia 640 LTE (Windows 10) (Microsoft Edge)
  - HUAWEI P30 lite (Chrome for Android)
  - Samsung Galaxy Tab A (Chrome for Android & Samsung Internet)
  - Lenovo ThinkBook 13S (Chrome, Microsoft Edge & Firefox)

# Encountered Issues


# Web Accessibility

The website's homepage was tested to ensure it was accessible to people with disabilities using the [Web Accessibility](https://www.webaccessibility.com/) checker.

Overall, the home and about us pages received a very good score of 98 and 93% respectively.

<h2 align="center"><img src="readme/images/web_accessibility_score.jpg" alt="accessibility score" target="_blank" width="75%" height="75%"></h2>

<h2 align="center"><img src="readme/images/accessibility_about.jpg" alt="accessibility score" target="_blank" width="75%" height="75%"></h2>

# Performance Testing
Performance was tested using [Lighthouse](https://developers.google.com/web/tools/lighthouse) tool.

## Desktop

### Home page

<h2 align="center"><img src="readme/images/desktop_home.jpg" alt="lighthouse performance for home page" target="_blank" width="45%" height="45%"></h2>

### About Us page

<h2 align="center"><img src="readme/images/desktop_about.jpg" alt="lighthouse performance for about page" target="_blank" width="45%" height="45%"></h2>

For desktop performance, results were similar every time for both home and about pages.
The result is somewhat lover for 'Best Practices' due to Trust and Safety - the page 'Does not use HTTPS'. Since this is a project for educational purpose only it is not required to instal SSL certificate and therefore this warning can be ignored. 

The performance results are overall satisfying as the website is heavy loaded with the content.

## Mobile
### Home page

<h2 align="center"><img src="readme/images/mobile_home.jpg" alt="lighthouse performance for home page" target="_blank" width="45%" height="45%"></h2>

### About Us page

<h2 align="center"><img src="readme/images/mobile_about.jpg" alt="lighthouse performance for about page" target="_blank" width="45%" height="45%"></h2>

The mobile results were somewhat different every time. Following article [Why are my Lighthouse scores different from my other test results?](https://support.speedcurve.com/en/articles/4088236-why-are-my-lighthouse-scores-different-from-my-other-test-results#:~:text=The%20performance%20score%20is%20strongly,cause%20variability%20in%20your%20scores.) gives an explanation on Lighthouse that "the performance score is strongly influenced by Time to Interactive (TTI) and Total Blocking Time (TBT), which can be quite different depending on the test environment and runtime settings."

The performance results are overall satisfying as the website is heavy loaded with the content.

<br/>
Click here to return to [README.md](README.md) file.

