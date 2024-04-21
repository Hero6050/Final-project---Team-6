#!/usr/bin/env python
# coding: utf-8

# In[2]:


class Post:
    """
    Class to represent a social media post.
    """

    def __init__(self, post_id, datetime, content, author, views):
        """
        Initializes a Post object with provided attributes.

        Args:
            post_id (int): Unique identifier for the post.
            datetime (str): Date and time when the post was created.
            content (str): Text content of the post.
            author (str): Author of the post.
            views (int): Number of views the post has received.
        """
        # Initializing attributes of the post
        self.post_id = post_id  # Unique identifier for the post
        self.datetime = datetime  # Date and time when the post was created
        self.content = content  # Text content of the post
        self.author = author  # Author of the post
        self.views = views  # Number of views the post has received


class HashTable:
    """
    Hash table implementation for storing posts by datetime.
    """

    def __init__(self, size=10):
        """
        Initializes a HashTable object with a given size.

        Args:
            size (int): Size of the hash table.
        """
        # Initializing the size of the hash table and creating an empty table
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        """
        Hash function to convert a datetime string into an index.

        Args:
            key (str): Datetime string.

        Returns:
            int: Index for the given key.
        """
        # Calculating the hash value based on the sum of ASCII values of characters in the key
        hash_value = sum(ord(char) for char in key) % self.size
        return hash_value

    def insert(self, key, value, verbose=False):
        """
        Inserts a key-value pair into the hash table.

        Args:
            key (str): Key for the entry.
            value: Value associated with the key.
            verbose (bool): Whether to print verbose output. Default is False.
        """
        # Getting the index where the key-value pair will be inserted
        index = self._hash(key)
        node = self.table[index]

        # Handling collision by chaining
        if node is None:
            # If there is no collision, insert the key-value pair directly
            self.table[index] = [(key, value)]
            if verbose:
                print(f'{key} inserted without collision at {index}')
        else:
            # If there is a collision, append to the existing chain
            self.table[index].append((key, value))
            if verbose:
                print(f'{key} successfully inserted on chain at {index}')

    def search(self, key, verbose=False):
        """
        Searches for a value associated with a given key in the hash table.

        Args:
            key (str): Key to search for.
            verbose (bool): Whether to print verbose output. Default is False.

        Returns:
            The value associated with the key, if found. Otherwise, returns None.
        """
        # Getting the index where the key may be located
        index = self._hash(key)
        nodes = self.table[index]

        # Searching for the key in the chain at the calculated index
        if nodes is not None:
            for node in nodes:
                if node[0] == key:
                    return node[1]
                if verbose:
                    print(f'At hash value {index}, "{node[0]}" not equal to target.')
        return None


class BST:
    """
    Binary search tree implementation to store posts sorted by datetime.
    """

    class Node:
        """
        Represents a node in the binary search tree.
        """

        def __init__(self, post):
            """
            Initializes a Node object with a post.

            Args:
                post (Post): The post to be stored in the node.
            """
            self.post = post
            self.left = None
            self.right = None

    def __init__(self):
        """
        Initializes a BST object.
        """
        # Initializing the root of the binary search tree
        self.root = None

    def insert(self, post):
        """
        Inserts a post into the binary search tree.

        Args:
            post (Post): The post to be inserted.
        """
        if not self.root:
            # If the tree is empty, set the post as the root
            self.root = self.Node(post)
        else:
            # Otherwise, insert recursively based on datetime
            self._insert_recursive(self.root, post)

    def _insert_recursive(self, current_node, post):
        """
        Recursively inserts a post into the binary search tree.

        Args:
            current_node (Node): The current node being processed.
            post (Post): The post to be inserted.
        """
        if post.datetime < current_node.post.datetime:
            # If the post's datetime is less than current node's datetime, insert to the left
            if current_node.left is None:
                current_node.left = self.Node(post)
            else:
                self._insert_recursive(current_node.left, post)
        else:
            # If the post's datetime is greater or equal, insert to the right
            if current_node.right is None:
                current_node.right = self.Node(post)
            else:
                self._insert_recursive(current_node.right, post)

    def find_posts_in_range(self, start_datetime, end_datetime):
        """
        Finds posts within a given datetime range.

        Args:
            start_datetime (str): The starting datetime of the range.
            end_datetime (str): The ending datetime of the range.

        Returns:
            list: List of posts within the given datetime range.
        """
        posts = []
        self._find_posts_in_range_recursive(self.root, start_datetime, end_datetime, posts)
        return posts

    def _find_posts_in_range_recursive(self, current_node, start_datetime, end_datetime, posts):
        """
        Recursively finds posts within a given datetime range.

        Args:
            current_node (Node): The current node being processed.
            start_datetime (str): The starting datetime of the range.
            end_datetime (str): The ending datetime of the range.
            posts (list): List to store the found posts.
        """
        if current_node is None:
            return

        if current_node.post.datetime >= start_datetime and current_node.post.datetime <= end_datetime:
            # If the post's datetime is within the range, add it to the list
            posts.append(current_node.post)

        if current_node.post.datetime > start_datetime:
            # Recursively search in the left subtree if necessary
            self._find_posts_in_range_recursive(current_node.left, start_datetime, end_datetime, posts)

        if current_node.post.datetime < end_datetime:
            # Recursively search in the right subtree if necessary
            self._find_posts_in_range_recursive(current_node.right, start_datetime, end_datetime, posts)


import heapq  # Importing heapq for priority queue operations


class MaxHeap:
    """
    Max heap implementation to store posts sorted by views.
    """

    def __init__(self):
        """
        Initializes a MaxHeap object.
        """
        # Initializing an empty heap
        self.heap = []

    def insert(self, post):
        """
        Inserts a post into the max heap.

        Args:
            post (Post): The post to be inserted.
        """
        # Inserting the post into the heap based on its views
        heapq.heappush(self.heap, (-post.views, post))

    def extract_max(self):
        """
        Extracts the post with the maximum views from the max heap.

        Returns:
            Post: The post with the maximum views.
        """
        if not self.heap:
            raise IndexError("Cannot extract from an empty heap")
        return heapq.heappop(self.heap)[1]

    def peek_max(self):
        """
        Returns the post with the maximum views without removing it from the heap.

        Returns:
            Post or None: The post with the maximum views, or None if the heap is empty.
        """
        if not self.heap:
            return None
        return self.heap[0][1]

    def display_sorted(self):
        """
        Displays the posts in the heap sorted by views.
        """
        # Sorting the heap based on views and displaying the posts
        sorted_heap = sorted(self.heap, key=lambda x: x[1].views, reverse=True)
        for _, post in sorted_heap:
            # Printing post details
            print(f"Post: {post.content} by {post.author}, Views: {post.views}")


class SocialMediaManager:
    """
    Class to manage social media posts.
    """

    def __init__(self):
        """
        Initializes a SocialMediaManager object with data structures to store posts.
        """
        # Initializing hash table, binary search tree, and max heap
        self.hash_table = HashTable()
        self.bst = BST()
        self.posts_heap = MaxHeap()

    def add_post(self, post_id, datetime, content, author, views):
        """
        Adds a post to the social media manager.
        """
        # Creating a Post object and inserting it into hash table, binary search tree, and max heap
        post = Post(post_id, datetime, content, author, views)
        self.hash_table.insert(datetime, post)
        self.bst.insert(post)
        self.posts_heap.insert(post)

    def get_post_by_datetime(self, datetime):
        """
        Retrieves a post by its datetime.
        """
        # Searching for the post in the hash table and displaying its details if found
        post_by_datetime = self.hash_table.search(datetime)
        if post_by_datetime:
            print("\nPost found by datetime:")
            print(f"DateTime: {post_by_datetime.datetime}")
            print(f"Post: {post_by_datetime.content}")
            print(f"Poster: {post_by_datetime.author}")
            print(f"Views: {post_by_datetime.views}")
        else:
            print("Post not found")
        return post_by_datetime

    def find_posts_in_range(self, start_datetime, end_datetime):
        """
        Finds posts within a given datetime range.
        """
        # Finding posts within the range in the binary search tree and displaying their details
        posts_in_range = self.bst.find_posts_in_range(start_datetime, end_datetime)
        if posts_in_range:
            print("\nPosts found in range:")
            for post in posts_in_range:
                print(
                    f"ID: {post.post_id}, DateTime: {post.datetime}, Post: {post.content}, Poster: {post.author}, Views: {post.views}")
        else:
            print("No posts found in range")

    def get_most_viewed_post(self):
        """
        Retrieves the most viewed post.
        """
        # Getting the most viewed post from the max heap and displaying its details
        most_viewed_post = self.posts_heap.peek_max()
        if most_viewed_post:
            print("\nMost viewed post:")
            print(f"DateTime: {most_viewed_post.datetime}")
            print(f"Post: {most_viewed_post.content}")
            print(f"Poster: {most_viewed_post.author}")
            print(f"Views: {most_viewed_post.views}")
        else:
            print("No posts available")


if __name__ == "__main__":
    # Create a social media manager
    social_media_manager = SocialMediaManager()

    # Add some posts
    social_media_manager.add_post(1, "2024-04-13 01:00:00", "Check out this Sunset photo!", "Asma", 100)
    social_media_manager.add_post(2, "2024-04-14 11:00:00", "New Youtube Video", "Brook", 15000)
    social_media_manager.add_post(3, "2024-04-14 11:00:00", "New song released", "Taylor", 22000)
    social_media_manager.add_post(4, "2024-04-15 13:00:00", "Photo dump from my Paris Trip", "Fakhra", 1200)
    social_media_manager.add_post(5, "2024-04-15 02:00:00", "Morning Coffee", "Khalfan", 1000)

    # Hash test cases
    print('1- Test retrieving a post by datetime (output - Post found by datetime)')
    post_by_datetime = social_media_manager.get_post_by_datetime("2024-04-13 01:00:00")

    print('2- Test retrieving a non-existent post by datetime (output - Post not found)')
    post_by_datetime = social_media_manager.get_post_by_datetime("2024-04-16 11:00:00")

    print('3- Test retrieving a post by datetime from a collison (output - Post found by datetime)')
    post_by_datetime = social_media_manager.get_post_by_datetime("2024-04-14 11:00:00")

    # BST test cases

    print('1-Test finding posts in a range (output - Posts found in range)')
    start_datetime = "2024-04-14 00:00:00"
    end_datetime = "2024-04-15 23:59:59"
    posts_in_range = social_media_manager.find_posts_in_range(start_datetime, end_datetime)

    print("2-Test finding posts in a range where no posts exist (output - No posts found in range)")
    start_datetime = "2024-04-16 00:00:00"
    end_datetime = "2024-04-17 00:00:00"
    posts_in_range = social_media_manager.find_posts_in_range(start_datetime, end_datetime)

    print("3-Test finding posts in a very small range")
    start_datetime = "2024-04-14 11:00:00"
    end_datetime = "2024-04-14 11:00:00"
    posts_in_range = social_media_manager.find_posts_in_range(start_datetime, end_datetime)

    # Maxheap test cases

    print("1- Test Display the Heap with sorted order of most views:")
    social_media_manager.posts_heap.display_sorted()

    print("2-Test extracting the post with the maximum views")
    pop_post = social_media_manager.posts_heap.extract_max()
    print(f"Post: {pop_post.content} by {pop_post.author}, Views: {pop_post.views}")

    print("3- Test Display the post with the most views:")
    social_media_manager.get_most_viewed_post()