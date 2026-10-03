# Erdős 699：GitHubからの全進展

2026年10月3日のまとめ。GitHubの研究記録と、その後のi=3・i=4・i=5の全追加研究、原本、証明書、検算コード、結果を同梱しています。

**一般i=5は未解決。最後の支持は{0,1}で、続行により45類を閉じ、必要合同類を9・64へ絞りました。**
問題全体の未解決添字は28個のままです。

まず次の順に読んでください。

1. [GitHub基準からの全追加成果・配布内容](docs/GITHUB_PROGRESS_2026-10-03.md)
2. [全研究のAI引き継ぎ](docs/AI_HANDOFF_2026-10-02.md)
3. [現在の成立範囲と未解決境界](docs/STATUS.md)
4. [証明・コードの検算手順](docs/VERIFICATION.md)

最新i=5の証明は [積・付値・有理直線近傍の閉鎖](research/i5/i5_global_product_and_affine_exclusions_2026-10-03.md)。全nの $j\le1.4\cdot10^{57}$ と中央近傍を閉じ、復元余因子の不均衡を強制しました。先行する証明は [四次・六次による支持02の閉鎖・第13節](research/i5/i5_multiplicity_frontier_2026-10-03.md)。
外部Bennett–Filaseta–Trifonov Theorem 2.1への依存を明示し、具体的な曲線・非零性・定数・全セル被覆は厳密に検算しました。

さらに最新稿の第9節で、**n−1,n,n＋1のいずれかが完全冪となる全域** と **n=3^f5^dの全f,d** を閉じました。残る一般枝の計算可能な上限は未取得です。

GitHubは2026-10-03に再照会しました。mainの基準はcf00db1d6edda7f28787114ab85c9199c48a1156で、手元の基準Git treeと一致します。追加研究はGitHubへpushしていません。
受領ZIPのSHA256.jsonとBUILD_METADATA.jsonは[原本保存フォルダ](archive/attachments/all_progress_2026-10-03/README.md)に保存しました。これらは受領した配布版の照合・commit・作成時点を記録します。この作業フォルダへの統合結果と32件の再検算は[統合記録](docs/IMPORT_2026-10-03.md)を参照してください。
Git管理情報・実行環境・一時探索ファイルは同梱していません。研究の再現に必要なソースと保存結果は同梱しています。
