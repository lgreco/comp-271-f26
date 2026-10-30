public class BinarySearchTree {
    
    private Node root;
    private int size;

    public BinarySearchTree() {
        this.root = null;
        this.size = 0;
    }

    public void insert(String value) {
        // new_node = Node(value)
        Node newNode = new Node(value);
        this.root = this.insertRec(this.root, newNode);
    }

    private Node insertRec(Node currentNode, Node newNode) {
        if (currentNode == null) {
            this.size++;
            currentNode = newNode;
        } else {
            
        }
        return currentNode;
    }
}
