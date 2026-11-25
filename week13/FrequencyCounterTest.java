/**
 * Given tests for Week 13. Run with:  javac *.java  then  java FrequencyCounterTest
 * Do not change this file. Each line of output says ok or FAIL.
 * Most tests fail on the untouched scaffold; that is expected.
 * These tests check countFrequency only. Check printFrequencies by running
 * java FrequencyCounter and reading what it prints.
 */
public class FrequencyCounterTest {

    // How many checks passed, and how many were run.
    private static int passed = 0;
    private static int total = 0;

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

    /** Adds up every slot of a counts array. */
    private static int sum(int[] counts) {
        int total = 0;
        for (int count : counts) {
            total += count;
        }
        return total;
    } // method sum

    public static void main(String[] args) {
        // --- The message from class ---------------------------------------
        int[] hello = FrequencyCounter.countFrequency("hello world");
        check("the array has 128 slots, one per ASCII character", hello.length == 128);
        check("'l' occurs 3 times", hello['l'] == 3);
        check("'o' occurs 2 times", hello['o'] == 2);
        check("'h' occurs once", hello['h'] == 1);
        check("'d', the last character, is counted", hello['d'] == 1);
        check("the space is a character too, and occurs once", hello[' '] == 1);
        check("'z' does not occur", hello['z'] == 0);
        check("the counts add up to the length (11)", sum(hello) == 11);

        // --- Edge cases ------------------------------------------------------
        int[] empty = FrequencyCounter.countFrequency("");
        check("an empty message still gives 128 slots", empty.length == 128);
        check("an empty message counts nothing", sum(empty) == 0);

        int[] repeated = FrequencyCounter.countFrequency("aaaa");
        check("one character repeated: 'a' occurs 4 times", repeated['a'] == 4);

        int[] mixed = FrequencyCounter.countFrequency("Aa");
        check("capitals are different characters: 'A' once", mixed['A'] == 1);
        check("capitals are different characters: 'a' once", mixed['a'] == 1);

        // 'é' is character 233, past the last slot. Without a check, counts[233]
        // throws an exception; we catch it so the remaining output still prints.
        boolean skipped;
        try {
            skipped = sum(FrequencyCounter.countFrequency("café")) == 3;
        } catch (ArrayIndexOutOfBoundsException e) {
            skipped = false;
        }
        check("a character outside ASCII is skipped, not a crash", skipped);

        System.out.println("\n" + passed + " of " + total + " checks passed.");
    } // method main
}
