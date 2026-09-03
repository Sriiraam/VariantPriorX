process SCORE_VARIANTS {

    tag "VariantPriorX scoring"

    input:
    path master

    output:
    path "variantpriorx_ranked.tsv"

    script:
    """
    mkdir -p results/annotation

    cp ${master} results/annotation/variantpriorx_master.tsv

    python ${projectDir}/scripts/score_variants.py

    cp results/annotation/variantpriorx_ranked.tsv \
       variantpriorx_ranked.tsv
    """
}
