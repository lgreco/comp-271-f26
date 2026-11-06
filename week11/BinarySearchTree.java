/**
 * A binary search tree of strings, ordered according to
 * {@link String#compareTo(String)}.
 * Each node's left and right links represent smaller and larger subtrees,
 * respectively.
 */
public class BinarySearchTree {

    /**
     * The root is the entry point to every node in the tree; null means empty.
     */
    private Node root;
    /** Track stored nodes separately so size can be reported without 
     * traversing the tree.
     */
    private int size;

    /** Creates an empty tree. */
    public BinarySearchTree() {
        this.root = null;
        this.size = 0;
    }

    /**
     * Starts inserting a value by creating its node and recursing from the root.
     *
     * @param value string to insert into the tree
     */
    public void insert(String value) {
        // new_node = Node(value)
        Node newNode = new Node(value);
        // The returned subtree root becomes the tree root (especially when inserting
        // first).
        this.root = this.insertRec(this.root, newNode);
    }


    /**
     * Recursively finds an insertion point and returns the root of the resulting
     * subtree.
     * Returning the subtree root lets each recursive caller reconnect the updated
     * child link.
     *
     * @param currentNode root of the subtree currently being examined, or
     *                    {@code null}
     * @param newNode     node to insert into the subtree
     * @return root of the subtree after the insertion step
     */
    private Node insertRec(Node currentNode, Node newNode) {
        if (currentNode == null) {
            // An empty link is the insertion point; adding here increases 
            // the node count once.
            this.size++;
            currentNode = newNode;
        } else {
            // Compare values and recurse into the matching side, then 
            // store its returned root in that child link. Node.compareTo 
            // defines the value ordering used by this tree.
        }
        return currentNode;
    }
}
