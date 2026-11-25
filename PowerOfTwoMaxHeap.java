import java.util.Arrays;
import java.util.NoSuchElementException;

/** Array-backed max heap of integers with 2^branchingExponent child slots per node. */
public final class PowerOfTwoMaxHeap {
    private static final int MAX_ARRAY_LENGTH = Integer.MAX_VALUE - 8;

    private final int indexShift;
    private final long branchingFactor;
    private int[] elements = new int[16];
    private int size;

    public PowerOfTwoMaxHeap(int branchingExponent) {
        if (branchingExponent < 0) {
            throw new IllegalArgumentException("branchingExponent must be nonnegative");
        }
        // At 2^31 child slots or more, every possible array element after
        // the root is its child. A shift of 31 yields the same array layout.
        indexShift = Math.min(branchingExponent, 31);
        branchingFactor = 1L << indexShift;
    }

    public void insert(int value) {
        if (size == elements.length) {
            if (size == MAX_ARRAY_LENGTH) {
                throw new IllegalStateException("Heap has reached maximum capacity");
            }
            long grownLength = (long) size + (size >>> 1) + 1;
            elements = Arrays.copyOf(elements, (int) Math.min(grownLength, MAX_ARRAY_LENGTH));
        }

        int index = size++;
        while (index > 0) {
            int parent = (index - 1) >>> indexShift;
            if (elements[parent] >= value) {
                break;
            }
            elements[index] = elements[parent];
            index = parent;
        }
        elements[index] = value;
    }

    public int popMax() {
        if (size == 0) {
            throw new NoSuchElementException("Heap is empty");
        }

        int maximum = elements[0];
        int replacement = elements[--size];
        if (size == 0) {
            return maximum;
        }

        int index = 0;
        while (true) {
            long firstChild = ((long) index << indexShift) + 1;
            if (firstChild >= size) {
                break;
            }

            int largestChild = (int) firstChild;
            int childLimit = (int) Math.min(firstChild + branchingFactor, size);
            for (int child = largestChild + 1; child < childLimit; child++) {
                if (elements[child] > elements[largestChild]) {
                    largestChild = child;
                }
            }

            if (elements[largestChild] <= replacement) {
                break;
            }
            elements[index] = elements[largestChild];
            index = largestChild;
        }
        elements[index] = replacement;
        return maximum;
    }
}
