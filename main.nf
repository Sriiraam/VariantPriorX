nextflow.enable.dsl=2

include { BUILD_MASTER }    from './modules/build_master'
include { SCORE_VARIANTS }  from './modules/score_variants'
include { BUILD_DATABASE }  from './modules/build_database'

workflow {

    vep_ch = Channel.fromPath(
        params.vep_candidates,
        checkIfExists: true
    )

    clinvar_ch = Channel.fromPath(
        params.clinvar_annotations,
        checkIfExists: true
    )

    gnomad_ch = Channel.fromPath(
        params.gnomad_frequency,
        checkIfExists: true
    )

    BUILD_MASTER(
        vep_ch,
        clinvar_ch,
        gnomad_ch
    )

    SCORE_VARIANTS(
        BUILD_MASTER.out
    )

    BUILD_DATABASE(
        SCORE_VARIANTS.out
    )
}
