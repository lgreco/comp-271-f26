
public class Node implements Comparable<Node> {

    private String value;
    private Node left;
    private Node right;

    /**
     * This is the constructor a simple binary search tree node;
     * Initially, left and right children are null
     * @param value String with the data payload for the node
     */
    public Node(String value) {
        this.value = value;
        this.left = null;
        this.right = null;
    }

    public String toString() {
        return this.value;
    }

    public int compareTo(Node other) {
        return this.value.compareTo(other.value);
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    public Node getLeft() {
        return left;
    }

    public void setLeft(Node left) {
        this.left = left;
    }

    public Node getRight() {
        return right;
    }

    public void setRight(Node right) {
        this.right = right;
    }


}
