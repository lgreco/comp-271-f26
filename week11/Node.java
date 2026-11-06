/**
 * One string-valued node in a binary search tree, with links to its child
 * subtrees.
 * Nodes compare according to the natural ordering of their string values.
 */
public class Node implements Comparable<Node> {

    // Each node stores one value and links to the roots of its left and right
    // subtrees.
    private String value;
    private Node left;
    private Node right;

    /**
     * Creates a node with no children.
     *
     * @param value string stored in this node
     */
    public Node(String value) {
        // Store the string we were given. 'this.value' is the field; 'value' is the
        // parameter. 'this' is Java's version of Python's 'self', and here it is required.
        this.value = value;
        // A brand-new node has no children yet; null is Java's None.
        this.left = null;
        this.right = null;
    }

    /**
     * Returns the stored string in brackets, which is the node's readable
     * representation.
     *
     * @return this node's value
     */
    @Override
    public String toString() {
        // '+' joins strings, like Python's. The brackets make a node easy to spot in output.
        return "[ " + this.value + " ]";
    }

    /**
     * Compares this node's value with another node's value using string ordering.
     *
     * @param other node whose value is compared with this node's value
     * @return a negative number, zero, or a positive number when this value is less
     *         than, equal to, or greater than the other value
     */
    @Override
    public int compareTo(Node other) {
        // Delegate to String.compareTo: compare the contents, not the node objects.
        // Negative: this value sorts first. Zero: equal. Positive: this value sorts later.
        return this.value.compareTo(other.value);
    }

    /** @return the string stored in this node */
    public String getValue() {
        // Accessor: the field is private, so other classes must ask for it.
        return value;
    }

    /** @param value new string to store in this node */
    public void setValue(String value) {
        this.value = value;
    }

    /** @return the left child, or {@code null} if there is no left child */
    public Node getLeft() {
        return left;
    }

    /**
     * @param left new root of the left subtree, or {@code null} to clear the link
     */
    public void setLeft(Node left) {
        this.left = left;
    }

    /** @return the right child, or {@code null} if there is no right child */
    public Node getRight() {
        return right;
    }

    /**
     * @param right new root of the right subtree, or {@code null} to clear the link
     */
    public void setRight(Node right) {
        this.right = right;
    }
}
