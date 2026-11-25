/**
 * Counts how often each character occurs in a message: the Java version of
 * count_freq in encoding.py (class of 11/16).
 *
 * The Python version kept its counts in a dict. This one keeps them in a
 * plain array of 128 ints, one slot per ASCII character. That works because
 * in Java a char IS a small whole number: 'a' is 97, 'b' is 98, ' ' is 32.
 * So counts['a'] is the same slot as counts[97], and holds how many a's we saw.
 *
 * Run with:  javac *.java  then  java FrequencyCounterTest
 * Or try your own message:  java FrequencyCounter "your message here"
 */
public class FrequencyCounter {

    // One slot for every ASCII character, 0 through 127.
    public static final int ASCII_SIZE = 128;

    /**
     * Counts how many times each ASCII character occurs in a message.
     * Characters outside ASCII (such as 'é', which is 233) have no slot and are
     * skipped.
     *
     * @param message the text to count
     * @return an array of 128 counts; slot c holds the number of times the
     *         character c occurs in message
     */
    public static int[] countFrequency(String message) {
        // A new int array starts out all zeros: nothing counted yet.
        int[] counts = new int[ASCII_SIZE];

        // TODO: walk the message one character at a time, and add 1 to the
        // slot for that character. Skip any character that has no slot.
        // Useful: message.length() and message.charAt(i).

        return counts;
    } // method countFrequency

    /**
     * Prints one line for every character that occurs in the message, in ASCII
     * order, showing the character in quotes and its count, like this:
     *
     *   ' ' 1
     *   'd' 1
     *   'e' 1
     *
     * Characters that never occur (count 0) are not printed.
     *
     * @param counts an array of 128 counts, as returned by countFrequency
     */
    public static void printFrequencies(int[] counts) {
        // TODO: print the non-zero slots. To print slot i as a character
        // rather than as a number, cast it: (char) i
    } // method printFrequencies

    /**
     * Counts and prints the frequencies of a message: the one given on the
     * command line, or "hello world" if none is given.
     *
     * @param args optional message, typed in quotes after the program name
     */
    public static void main(String[] args) {
        String message = "hello world";
        if (args.length > 0) {
            message = args[0];
        }
        System.out.println("Frequencies in \"" + message + "\":");
        printFrequencies(countFrequency(message));
    } // method main
}
