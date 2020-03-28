# selection-test-posts-rest
Uses flask to make a REST endpoints to sort through posts from the bioinformatics.stackexchange.com website. 

## Installation
```
git clone https://github.com/jshin313/selection-test-posts-rest selection-test
cd selection-test
pip install -r requirements.txt 
```

## Usage
```
python3 app.py
# Then go to localhost:5000/posts
```

## Examples
```
# Returns default which is sorted by creation date
http://localhost:5000/posts 

# Returns posts sorted by view count
http://localhost:5000/posts?byViewCount=true 

# Returns posts sorted by score
http://localhost:5000/posts?byScore=true 

# Searches for all instances where "RNA" is in the title (Case insensitive)
http://localhost:5000/posts?searchTitle=RNA 

# Searches for all instances where "biology" is in the body (Case insensitive)
http://localhost:5000/posts?searchBody=biology 

# Searches for all instances where "hello" is in the body or title (Case insensitive)
http://localhost:5000/posts?search=hello ```

