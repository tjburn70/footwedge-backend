## Build Process

Beautiful Soup has a dependency of lxml, which does not play well with aws lambda.
We need to utilize a precompiled binary.

We are the using the precompiled binary for runtime Python 3.6 found here: https://github.com/JFox/aws-lambda-lxml

Our build process will utilize our Pipfile to determine the requirements.txt for our lambda.

After installing our dependencies into the ```target/``` dir, we will replace
the lxml package with the precompiled binary found in our ```static/``` dir.
