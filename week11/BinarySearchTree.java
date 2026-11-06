/**
 * A binary search tree of strings, ordered according to
 * {@link String#compareTo(String)}.
 * Each node's left and right links represent smaller and larger subtrees,
 * respectively. Inserting a value that is already stored does not add a node:
 * the tree records the repeat (Week 11, Part B).
 */
public class BinarySearchTree {

    /**
     * The root is the entry point to every node in the tree; null means empty.
     */
    private Node root;
    /**
     * Track stored nodes separately so size can be reported without
     * traversing the tree. This is the number of DISTINCT values.
     */
    private int size;

    /** Creates an empty tree. */
    public BinarySearchTree() {
        // An empty tree has no root and no nodes. null is Java's None.
        this.root = null;
        this.size = 0;
    }

    /** Accessor for the size of the tree. */
    public int getSize() {
        // The field is private, so callers use this accessor instead.
        return this.size;
    } // method getSize

    /**
     * Starts inserting a value by creating its node and recursing from the root.
     *
     * @param value string to insert into the tree
     */
    public void insert(String value) {
        // Python: new_node: Node = Node(value)
        // Java needs the type on both sides: the variable's, and the new object's.
        Node newNode = new Node(value);
        // The returned subtree root becomes the tree root. That is what makes the
        // very first insert work (an empty tree returns the new node) and it
        // leaves the root unchanged on every insert after that.
        this.root = this.insertRec(this.root, newNode);
    } // method insert

    /**
     * Recursively finds an insertion point and returns the root of the resulting
     * subtree. Returning the subtree root lets each recursive caller reconnect
     * the updated child link.
     *
     * @param currentNode root of the subtree currently being examined, or
     *                    {@code null}
     * @param newNode     node to insert into the subtree
     * @return root of the subtree after the insertion step
     */
    private Node insertRec(Node currentNode, Node newNode) {
        if (currentNode == null) {
            // An empty link is the insertion point. The new node becomes this
            // subtree, and the node count goes up by one.
            this.size++;
            currentNode = newNode;
        } else if (newNode.compareTo(currentNode) < 0) {
            // Smaller: go left. The recursive call returns the root of the left
            // subtree after the insertion; store it back as the left child.
            // currentNode is NOT overwritten: it is the node this call must
            // return, so the parent keeps its link to it.
            currentNode.setLeft(this.insertRec(currentNode.getLeft(), newNode));
        } else if (newNode.compareTo(currentNode) > 0) {
            // Larger: go right, and store the result as the right child.
            currentNode.setRight(this.insertRec(currentNode.getRight(), newNode));
        } else {
            // PART B (frequency): compareTo returned 0, so the value is already
            // in the tree. Right now the duplicate is simply dropped (the new
            // node is thrown away). Decide what this branch should do so the
            // tree remembers the repeat.
            // size counts distinct values, so size must not change.
        }
        // Return this subtree's root: the new node in the base case, otherwise
        // the node we were given. One return, at the end.
        return currentNode;
    } // method insertRec

    /**
     * PART A: reports whether a value is stored in the tree.
     *
     * Hint: the public method wraps the value in a Node and starts the
     * recursion at the root, exactly as insert does. The private helper
     * searchRec does the real work.
     *
     * @param value string to look for
     * @return true if the value is in the tree, false otherwise
     */
    public boolean search(String value) {
        boolean found = false; // pessimistic: assume the value is not there
        // TODO: replace the next line with your code.
        found = false;
        return found;
    } // method search

    /**
     * PART A: recursive helper for search.
     *
     * Hint: two base cases (an empty subtree means the value is absent; a
     * matching node means it is present), otherwise compare and search the
     * left or the right subtree. Use compareTo and keep exactly one return.
     * Python guarded against None with "node is not None and ..."; in Java
     * the guard is "currentNode != null &&", and && does not evaluate its
     * right side when the left side is already false.
     *
     * @param currentNode root of the subtree being searched, or {@code null}
     * @param target      node holding the value being looked for
     * @return true if the target's value is in the subtree
     */
    private boolean searchRec(Node currentNode, Node target) {
        boolean found = false; // pessimistic default
        // TODO: replace the next line with your code.
        found = false;
        return found;
    } // method searchRec

    /**
     * PART B: reports how many times a value has been inserted.
     *
     * Hint: it descends the tree like search.
     *
     * @param value string to look for
     * @return number of insertions of the value; 0 if it was never inserted
     */
    public int frequency(String value) {
        int occurrences = 0; // pessimistic: assume the value is not there
        // TODO: replace the next line with your code.
        occurrences = 0;
        return occurrences;
    } // method frequency
}
