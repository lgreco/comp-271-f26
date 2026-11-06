/**
 * Given tests for Week 11. Run with:  javac *.java  then  java BinarySearchTreeTest
 * Do not change this file. Each line of output says ok or FAIL with a reason.
 * Some tests fail on the untouched scaffold; that is expected.
 */
public class BinarySearchTreeTest {

    // How many checks passed, and how many were run.
    private static int passed = 0;
    private static int total = 0;

    // The opening line of Richard III, as used in class (lower case).
    private static final String LINE = "now is the winter of our discontent made glorious summer "
            + "by this sun of york and all the clouds that loured upon our house "
            + "in the deep bosom of the ocean buried";

    /** Records one check: prints ok or FAIL and updates the counters. */
    private static void check(String name, boolean condition) {
        total++;
        if (condition) {
            passed++;
            System.out.println("  ok    " + name);
        } else {
            System.out.println("  FAIL  " + name);
        }
    } // method check

    /** Builds a tree from the words of a string. */
    private static BinarySearchTree build(String text) {
        BinarySearchTree tree = new BinarySearchTree();
        for (String word : text.split(" ")) {
            tree.insert(word);
        }
        return tree;
    } // method build

    public static void main(String[] args) {
        // --- Part A: search -------------------------------------------
        BinarySearchTree empty = new BinarySearchTree();
        check("search: an empty tree contains nothing", !empty.search("now"));

        BinarySearchTree one = build("hello");
        check("search: finds the only value (the root)", one.search("hello"));
        check("search: does not find a value that is absent", !one.search("world"));

        BinarySearchTree tree = build(LINE);
        check("search: finds the first word inserted", tree.search("now"));
        check("search: finds the last word inserted", tree.search("buried"));
        check("search: finds a word deep on the left", tree.search("all"));
        check("search: finds a word deep on the right", tree.search("upon"));
        check("search: absent word between two stored words", !tree.search("moon"));
        check("search: absent word smaller than everything", !tree.search("aardvark"));
        check("search: absent word larger than everything", !tree.search("zebra"));
        check("search: capitals matter ('Now' is not 'now')", !tree.search("Now"));

        // Insert order must not matter: build the same words backwards.
        String[] words = LINE.split(" ");
        BinarySearchTree backwards = new BinarySearchTree();
        boolean everyWordFound = true;
        for (int i = words.length - 1; i >= 0; i--) {
            backwards.insert(words[i]);
        }
        for (String word : words) {
            everyWordFound = everyWordFound && backwards.search(word);
        }
        check("search: every inserted word is found, whatever the order", everyWordFound);

        // --- Part B: frequency ----------------------------------------
        check("frequency: a word inserted once", tree.frequency("winter") == 1);
        check("frequency: 'the' appears 4 times", tree.frequency("the") == 4);
        check("frequency: 'of' appears 3 times", tree.frequency("of") == 3);
        check("frequency: 'our' appears 2 times", tree.frequency("our") == 2);
        check("frequency: an absent word is 0", tree.frequency("zebra") == 0);
        check("frequency: an empty tree gives 0", empty.frequency("now") == 0);
        check("size: counts distinct words only (26 of 32)", tree.getSize() == 26);

        BinarySearchTree again = build("a a a");
        check("size: three inserts of one word make size 1", again.getSize() == 1);
        check("frequency: three inserts of one word make 3", again.frequency("a") == 3);

        System.out.println("\n" + passed + " of " + total + " checks passed.");
    } // method main
}
