process BUILD_DATABASE {

    tag "SQLite database"

    input:
    path ranked

    output:
    path "variantpriorx.db"

    script:
    """
    mkdir -p results/annotation database

    cp ${ranked} results/annotation/variantpriorx_ranked.tsv

    python ${projectDir}/scripts/build_database.py

    cp database/variantpriorx.db \
       variantpriorx.db
    """
}
