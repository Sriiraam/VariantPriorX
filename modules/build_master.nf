process BUILD_MASTER {

    tag "Merge VEP + ClinVar + gnomAD"

    input:
    path vep
    path clinvar
    path gnomad

    output:
    path "variantpriorx_master.tsv"

    script:
    """
    mkdir -p results/annotation

    cp ${vep} results/annotation/vep_clinical_candidates.tsv
    cp ${clinvar} results/annotation/clinvar_annotations.tsv
    cp ${gnomad} results/annotation/gnomad_frequency.tsv

    python ${projectDir}/scripts/build_master_table.py

    cp results/annotation/variantpriorx_master.tsv \
       variantpriorx_master.tsv
    """
}
