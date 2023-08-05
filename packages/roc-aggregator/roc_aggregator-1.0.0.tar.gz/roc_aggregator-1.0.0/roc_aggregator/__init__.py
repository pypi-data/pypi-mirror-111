""" ROC Aggregator

    Aggregates ROCs from multiple validations into one unique ROC.
"""
import numpy as np

from roc_aggregator.validations import validate_input

def partial_cm(fpr, tpr, thresholds, negative_count, total_count, descending=False):
    """ Compute the partial confusion matrix from the tpr and fpr.
    """
    # Arrange the necessary parameters
    node_indexes = np.repeat(range(len(thresholds)), [len(th) for th in thresholds])
    thresholds_stack = np.hstack(thresholds)

    shift = 0
    acc = np.zeros((len(thresholds_stack), 2))
    for i, node_thresholds in enumerate(thresholds):
        # Shift the index and thresholds according to the node
        # Necessary to guarantee that the current node thresholds
        # are always consider first when sorted
        node_indexes_shifted = np.flip(np.roll(node_indexes, -shift))
        thresholds_stack_shifted = np.flip(np.roll(thresholds_stack, -shift))
        # Sort all the thresholds
        sorted_indexes = np.argsort(thresholds_stack_shifted)[::-1]
        # Build an index list based on the i node values by doing a cumulative sum
        sum = np.cumsum(np.equal(node_indexes_shifted, i)[sorted_indexes]) - 1
        # Calculating and sort by threshold the tp and fp for the node
        cm = np.multiply(
            np.column_stack([np.array(fpr[i]), np.array(tpr[i])]),
            [negative_count[i], total_count[i] - negative_count[i]]
        )
        cm_sorted = np.append(
            cm[np.argsort(node_thresholds)[::-1]],
            [[cm[0][0], cm[0][1]]],
            axis=0
        )
        # Add the tp and fp values to the global array
        acc += cm_sorted[sum, :]
        # Increment the shift
        shift += len(node_thresholds)

    # Sort the tresholds and remove repeated entries
    thresholds_stack_sorted, unique_ind = np.unique(
        np.sort(thresholds_stack)[::-1] if descending else np.sort(thresholds_stack),
        return_index=True
    )

    if descending:
        cm = acc[unique_ind[::-1], :]
        thresholds_stack_sorted = thresholds_stack_sorted[::-1]
    else:
        cm = acc[::-1][unique_ind, :]

    return cm, thresholds_stack_sorted

def roc_curve(fpr, tpr, thresholds, negative_count, total_count):
    """ Compute Receiver operating characteristic (ROC).

        Parameters
        ----------
        fpr: list - False positive rates for each individual ROC.
        tpr: list - True positive rates for each individual ROC.
        thresholds: list - Thresholds used to compute the fpr and tpr.
        negative_count: list - Total number of samples corresponding to the negative case.
        total_count: list - Total number of samples.

        Returns
        -------
        fpr_global: np.array() - The false positive rates for the global ROC.
        tpr_global: np.array() - The true positive rates for the global ROC.
        thresholds_stack: np.array() - The thresholds used to compute the fpr and tpr.

        Raises
        ------
        TypeError
            If the parameters' dimensions don't match.
    """
    #validate_input(fpr, tpr, thresholds, negative_count, total_count)
    # Obtain the partial confusion matrix (tp and fp)
    cm_partial, thresholds_stack = partial_cm(
        fpr, tpr, thresholds, negative_count, total_count, descending=True)
    
    # Compute the global fpr and tpr
    fpr_global = np.divide(cm_partial[:, 0], np.sum(negative_count))
    tpr_global = np.divide(cm_partial[:, 1], (np.sum(total_count) - np.sum(negative_count)))

    return fpr_global, tpr_global, thresholds_stack

def precision_recall_curve(fpr, tpr, thresholds, negative_count, total_count):
    """ Compute the precision recall curve.

        Parameters
        ----------
        fpr: list - False positive rates for each individual ROC.
        tpr: list - True positive rates for each individual ROC.
        thresholds: list - Thresholds used to compute the fpr and tpr.
        negative_count: list - Total number of samples corresponding to the negative case.
        total_count: list - Total number of samples.

        Returns
        -------
        fpr: np.array() - The false positive rates for the global ROC.
        tpr: np.array() - The true positive rates for the global ROC.
        thresholds_stack: np.array() - The thresholds used to compute the fpr and tpr.

        Raises
        ------
        TypeError
            If the parameters' dimensions don't match.
    """
    #validate_input(fpr, tpr, thresholds, negative_count, total_count)
    # Obtain the partial confusion matrix (tp and fp)
    cm_partial, thresholds_stack = partial_cm(fpr, tpr, thresholds, negative_count, total_count)

    # Compute the tpr/recall and precision
    pre_dividend = cm_partial[:, 1] + cm_partial[:, 0]
    pre = np.divide(cm_partial[:, 1], pre_dividend, out=np.ones(len(cm_partial)), where=pre_dividend!=0)
    recall = np.divide(cm_partial[:, 1], (np.sum(total_count) - np.sum(negative_count)))

    return pre, recall, thresholds_stack
