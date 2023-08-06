# **Py-linkedlist**

Work with linkedlists datastructure in Python

## **Installation**


```
pip install py-linkedlist
```

## **Import Package**

```
# Importing linkedlist to your code
from linkedlist import linkedlist
```

## **Creating First Linkedlist**

```
Initialising a linkedlist
l_list = linkedlist()
```

## **Adding Elements in the Linkedlist**

```
#Adding First element to the linkedlist
l_list.add(10)
```

```
# Appending a list to the linkedlist
l_list.add([1, 2])
```

```
# Appending a tuple to the linkedlist
l_list.add((3, 4, 3))
```

```
# Adding new element at head position in linkedlist
l_list.addAtHead(20)
```

```
Any data type including String, Dictonary, Sets etc. can be added to linkedlist
```

## **Printing the Linkedlist**

```
# Priting the linkedlist to console
l_list.show()

output: 20->10->1->2->3->4->3
```

## **Get Linkedlist length**

```
# Returns length of linkedlist
print(l_list.length())

output: 7
```

## **Deleting Linkedlist elements**

```
# Remove first occurance of an element (3) 
# l_list: 20->10->1->2->3->4->3

l_list.removeElement(3)
l_list.show()

output: 20->10->1->2->4->3
```

```
# Remove using element position 
# l_list: 20->10->1->2->4->3

l_list.removeAtLoc(2)
l_list.show()

output: 20->1->2->4->3
```

```
# Remove Head/First element in linkedlist 
# l_list: 20->1->2->4->3

l_list.removeHead()
l_list.show()

output: 1->2->4->3
```

```
# Remove Tail/Last element in linkedlist 
# l_list: 1->2->4->3

l_list.removeTail()
l_list.show()

output: 1->2->4
```

```
# Remove All elements in linkedlist 
# l_list: 1->2->4->3

l_list.removeAll()
l_list.show()

output: None
```

## **Checking Linkedlist is Empty/Not**

```
# Checking the linkedlist is Empty/Not

print(l_list.isEmpty())

output: True
```

## **Indexing Linkedlist element with location**

```
# Get Linkedlist with location. Linkedlist are zero-indexed based
l_list.add((13, 41, 34))
print(l_list.eleAt(2))

output: 34
```

## **Uninstall Package**

```
pip uninstall py-linkedlist
```
