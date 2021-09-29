# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        # FIXME: Write this function
        for i in range(self.capacity):              # Iterate through all buckets, reinitialize as empty LinkedLists
            self._buckets[i] = LinkedList()
        self.size = 0                               # Reset size counter

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        # FIXME: Write this function
        key_hash = self._hash_function(key)        # From "Exploration: Introduction to Maps and Hash Tables"
        index = key_hash % self.capacity
        node = self._buckets[index].contains(key)  # Check if key is present within table
        if node is not None:                       # If so, return value.
            return node.value
        return None                                # Otherwise None.


    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        # FIXME: Write this function
        newMap = HashMap(capacity, self._hash_function)         # Create new hash map with given capacity.
        for x in range(self.capacity):                          # Iterate through *old* hash map.
            cur = self._buckets[x].head                         # Traverse each bucket.
            while cur is not None:
                newMap.put(cur.key, cur.value)                  # Re-hash and add link to new hash map.
                cur = cur.next
        self._buckets = newMap._buckets                         # Finally, replace old with new.
        self.capacity = newMap.capacity

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """
        # FIXME: Write this function
        key_hash = self._hash_function(key)
        index = key_hash % self.capacity
        node = self._buckets[index].contains(key)               # Check for existence.
        if node is not None:
            node.value = value                                  # Update value if already present.
            return
        self._buckets[index].add_front(key, value)              # Otherwise add new link node.
        self.size += 1                                          # Increment hash map size.

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        # FIXME: Write this function
        key_hash = self._hash_function(key)
        index = key_hash % self.capacity
        if self._buckets[index].remove(key):                    # Check for removal success,
            self.size -= 1                                      # decrement hash map size if removed.

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        # FIXME: Write this function
        key_hash = self._hash_function(key)
        index = key_hash % self.capacity
        if self._buckets[index].contains(key):                  # After finding bucket index, can simply
            return True                                         # use LinkedList method to find.
        else:
            return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        # FIXME: Write this function
        cx = 0
        for x in range(self.capacity):
            if self._buckets[x].head is None:
                cx += 1                         # Increment for every unoccupied bucket,
        return cx                               # and return the count.

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        # FIXME: Write this function
        if self.size == 0:                      # Throws "divide by 0" error if not handled.
            return 0.0
        return self.size / self.capacity        # Table load definition

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out