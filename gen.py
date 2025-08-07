from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

def update():
    f = open("base.html", "r")
    base = f.read()
    f.close()

    f = open("template.html", "r")
    temp = f.read()
    f.close()

    style = temp.split("<!-- STYLE START -->\n")[1].split("\n<!-- STYLE END -->")[0]
    header = temp.split("<!-- HEADER START -->\n")[1].split("\n<!-- HEADER END -->")[0]
    body = temp.split("<!-- BODY START -->\n")[1].split("\n<!-- BODY END -->")[0]
    footer = temp.split("<!-- FOOTER START -->\n")[1].split("\n<!-- FOOTER END -->")[0]

    base = base.replace("[STYLE]", style)
    base = base.replace("[HEADER]", header)
    base = base.replace("[BODY]", body)
    base = base.replace("[FOOTER]", footer)

    vars = {
        "entity_footer": "",
        "company.logo": "data:image/png;base64,%20iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAgAElEQVR4nO3de3xV1Zk38N+z9smVQOEk3CJSBoUPo4z1tU4/La/ylhAuxctoC2gdBWtHafUFal+rojnpJifI2I7jgKMMtqggWhsYr0gRkmApo9YP5dV81KFAebkZArlAY8CQnL2e948kGJWQ276tk+f7+fBHFfd6mpz9nLWftfazACGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQvQGBR2A6NyejXZWf4WolYKoAuUQKKoJUWIVheJsYkRBNACMAQBA4CwmSgUQATgLAFr/XYRAERCyzlycuZGBxjP/m9AEoOGzfw8NonpibmKgHkA9E+rA3ACmv4JQT8z1INQz8wk4VO9oXXPkWEPV1+b8yyk/fj6i5yQBBGjPRjvrKxGMVhaNBKkRijAcjJEgyiXwCAZywIgSUSToWHuEuQHAYSYcI+AwM44B+FiDq4i5qtnhytoT2H/xbFsSRUAkAXhsz0Y7K5qGceDIRaR4DBFGgzGagQuJKCfo+EKBUQXifQzsZY2/MNNe4sTepubT+4bPWFoTdHjJTBKAS94uuTt9bPZXxhOpS8HqayAeR6BxIIwIOjazcT0De4mx2wHeZ0dXNOmmivOmLTkcdGTJQBJAD7y/5p7M3PMGXmaBvwHC/yDgUgaNI4KZU3UDMVAH5gqAKljz+8zOe3uO//Wjb81+tLHz/1q0kQTQBdWb4xdShL+poL4FwjfBuERu9vBhRgKEjwDerjX/V8Kht4ZNje0POq4wkwRwFoc2PJjbLzNtAhNNIcZUIhoVdEyihxhVDOwA4w8O67dOHtbvjrrVbgo6rLCQBABg/8v2gP5ZVj4pugrE+QQaGXRMwjOnGNgO1r/TzXpjzjR7d9ABBanPJoCjZfb4FERmQPFVYJogU/q+iRn7ibHJIX79aI1T3teWJPtUAqgpLbqcFGYR6LtEdGHQ8YhwYXATmLYx9CvOp7pkyFX2saBj8lrSJ4DazUXfQArdQMBMmdqLrmKwBqiUtX7uRO3Jly+Y/XB90DF5ISkTwOGNdm5GmppJSv2QgEuCjkeYjRmNAEpZY93hyhPrk2mLc9IkgLdL7k4fG82eTYp/ANBEIqigYxLJh8F1AP7j5MnGx8+/ekll0PH0lvEJ4Ngme7SVquYR1G1EkK21whcMNIH51WbNjwzNL3wn6Hh6ytgEULvF/oayrMUMmirf9iJIzHiTwUuy82KlQcfSXeYufVnqBhBNNzaDiaRBhG8DpAEYlwDkm1MINzAbeS8ZGbQQ4WPmXFQSgBBuIDNnAObWAESnWtavuZGABm5p9QUwaRDabWrhCPBZizAC0pkpkwgD/Y5X+E8SgDlOgXGQgcMAV4GphsHVBK7STDWaqYZVoh6MhqYEThw9UNlw+bwnE70ZcNcr92YNokgmRTKyVCpHNXGOAkUJyCFgMEHlsEIumHMJGMGgIX12RYbN/P8tCSAkmBlEOMhMu4mxl0n/2dG0WzMfbHL04fOn2yf8jmncP/yiAS0NQo8B2NfZ39+x8o7I8FGDh6VQ2khlqdGK9BiALiQkfws0MysAJicAMvVHzqfAqGCmXZr4z6Sx23F478Emvfvya2yju9m0zjgOt/5564v/fv/L9oB+GepCKwWjGepCAsYQ8TiAxgMtHY2NZejMx9wEYASuB/ABAzvYoT8168SOXW9h17dtWwcdWRBGXWfXA9jZ+udzDm14MDczI/UigC4ior8H0UUAjydQqv+R9h2SANzS0l9/B5i3M9EfmxN4T9pRdV3rvvpKtNtMs/8ZO7XfcDVepdAlBHwdRN8A+NJQJgWpAfiLNKlgf+Rcz0zvAvotZv7D7toT26UhpbtaW3e1zRieAVrqDCP+JndsiopcThZ/HaArWpOCkTdg0IxNAKxYk5+lF+YGJipn5i1NDkqHT4nt8m9w0aa1zvBR6581QOvZC+nWN4lwJZgmEuEbADL9jIvJzARkbALwA4N3AtjgOLzlwF8Ov9PbZTXhjTEz7Aa0PDqUAsCHJXYkJztyeQrxFQRMAmji545D8wR7e3mPGJsAvHgEYLAm4B3W9Ipu4pdzvhPr0w0jTXXxbDsB4J3WP//ypm2r8f8TlyoVyQdhCognul5HYJkBGI81/2t0cuHPgo5DuKt11aWtlvCL2rKiBaRombujmDkDMDJreUZRn1ye62sIHhy2amgNwMigAQBkZsYVoeDBzNfMz6O5CUCIHmIvEoChNQAjgxail2QG0EoSgOhzSMFy/6IyAxDCFDIDaGVwAjAz44rgeVEDIKkB+I1lyc5gx94ouqRqs31RQMPLDKCVwRuBzMy4okUkhaYSRX55fGv8I2Zef1rr3wzPt315v4K8+NwbWgMwOAEIk2kg0lKJo4uIqDDdUoVtyUA36+dyptlebsOWGUArSQAiEMSkvvwyZ0sysFLbJYPT9Jzb72QwEHH9PVJDawDmJgBimNuJTbR0Iz7X7681GaTjTDJwEvTs4Kmxvb0dmZgi7n90zJwBGJm1TPBhiW1ucvVB99bi6SIiVRhJoT3Ht8Y/rCsvWnxsY3x0z0dn1383pvYDMDJoE+TmWP+vdmt8ZXVp0RW2bQcdThj18CZsSQYpGfSXuq3Ff6otK1pwaMODuf6MfS4yAxDtMFGmAt0RsdQfFk60/ruuvGhx1eb4qKDjCgvm3n8LE3CZUmpZv8yMQ8e3xv+rtqxowcEt9rBOx5Z3Ac6QaapnOHHmGZdoHIEKUyMoOL41/g47WH2kzll78Wz7VLAxBsm9G6blMBKaoBRNyCL16PGt8Xe05t82NDeWfHX6Q1Vf+vsyAzhDEoBHiKnpi4Wmtg8qWZiQOzjyy7ry+KvMevVjf+DSvvaY4M1N+Plk0D8t40wySJxsfGHotQ8da/1rsg+glZFBm4CBzvoHDiCim5Wytiz8X9aB2vKih3tX2DIMe9CU4wtaOgXTBKXUspSsjI+Plxf/rra86FZ4cu6hzAD8FXhb8E51o4EojVRE91I67ml7RDh28pPnW4/mSk6KlZ/LuEQUATBdQU33ZABDawBGBm0CIm7q/n/T9ohAK4f2719dVx5fV1u2OD8ZHw88KcQFyswZgCQAjzCody3EidKJaKZS1paFEyOHasuLHq7eHL/QpfACRz48AvhKzgYUn8Pc5NoBpoQRCupelYJ767YW72StVzfWf7r2vOuX1rkzQBD8fQTwmqn/T4zMWgBC3xSUulUD6NZ1L1NKLcv4Sr+P68rj62rK41fvWHmHiYncxJg7ZujZgEYGDQDgcOdcJnS7BtAdREgnopkW0WsXjB15oG5rfNmxN4ou8XJMV2n8AcxfWqM3V7g/jx0xNwGEfAYA9mYG0IFcAi1ISVXvt22PPbJxUY6P43dbND/25JYVFeclHH0lg5cz2ODHGQDERt5LRgZtAgJ5OgPoeNyWR4S0jMyP68qLX6srL5oZ1heTZq9bpwfnF26PTootrD/gDHeYr2HmtQAM3CFp5gwglB+MZMBAIsiPBIFSQbgaUFfn5qiquq3xEkc7Tw+ebL8XYFgdaj0KfAOADQc23D8/Kz3rWlKYBWA6kQGfUzZzBhD+H6yx2r0LEDTCMAItiKjIguNb4x+xptXNJ089025rbKh89ep/PoGWo7/XHN5o52akqZlK0Q0ATQg6to6F5HfdTQYngHDvvGJCUzg/EnQRKTyc0j9jaV15cTmgV9Z+UP3qmAWPBfLI0pkRM+xKAMsBLD9Sao9LU+r7AN1ERKHaE8FSAxCfw/gVmLcHHUZHCKSIkE+k1mWPH/Jx3db4suoy+9Kg4zqX4fn2rmhe4c+jebExTiLx9dbiYUhmMeFM952RBOCR7LxY6aC82JWNCf5bBi8HI7T7+okop/UR4f8e3xr/sK6s+N4Dmx7o9L36IOVMsXdGJ8UWVvzeGa61M4WZ1wb6Mza0BmBm2gJQV178OBHudPOaGvyL7Emx+9y8Zpu/lNw3YFA060ayaCGAoPrhdxkzNIBy1nj2cOWJ9V+b8y+hr8zveM1OH91PXQ2ouQBPb30ByBfMqInmFQz2azy3SAJox8sE0F51adEVlqKFAF1nQoWbGScA3mBS74KPX1oUzeifOZMszGXGBHJrW3YHGFwXnRTL9nQQD5ibALbGHyeQkQmgzaEND+b2y0ybB9CdRBTqjTttGNgN1i80JejpYVNj+4OOpyuOvF48MjVdX0dEPyAiT+ocDNRFJxVIAvBLMiSANnuWz0/NHj/4WkDNI0K+3+P3BDM0ERvX3qxqs31RakTdANAcIhrl1nWZ+UQ0LzbIrev5RRJAO0ElgPaq3yi6TKXSPAXcDFBmkLF0Qz0zG9XerGTWLDVp3t9NsCyaBaabiNCrGRgzTkTzCiQB+MWLBMDMa4/UOD+4eLbt5z7+s9r/sj1gQJZ1Iym6G4RxQcfTdXxQM7/gNOmVQ6bb+4KOpiveLrk7fWx04AxS6hYQZhAotftX4fpBk2JfcT86b0kC+CJGlYZe09ykHx823T7o+vW7qWTWLDX5R+PziNQ8EL5LId8A1ab9I0Jtk/P8mBl2aJdB29v/sj2gf1bkuh5sQ64fNKlAEoBfPEsArdqWwQC9smKbfvHbth34ceTHNsZHW+k8j6Bu6+2U1U/MaAR4gwZWf7DN2RiGn2VXHNrwYG5mRlrXtiEzNwzKi/X3KTTXGJsAjpcVr4DCj/wYi4F90FjZ5CSeGjbVrvFjzHPZ/4ydOmCkupaI7g73/vizYBzW0M9rrX81ON/u9Tl/fvlsG7K6iQhf3obMaBiUVyAJwC9+JoA2DG4C41VmvTJ78s9L/Ry7IzVb7MsoYs1TjDkgSg86nu5gYCdrvfr0Kb029xrbmH4ANVvsy1TEmgvgRgINafmnfGrQpFi/QAPrAUkAPcXYpVmvqG5oeCoM7bsPbLh/YFZG5hwidTcRRgUdT3e0f0TYv+fQpsvnPRl4EbYr3rRt9XdXUh6RmgvC1Oik2NCgY+ouSQC9V8/gtc0JXjF0SuEHQQfzWdHQWgjw1V7vgPNAJYPXJ5qdVUOm2hVBB9NVO16z0y+/xm4MOo7uMu7T0SZECeAMBnbC4ZX7PnXWhOHDUL05fqGK8O1E9E8EigYdT/fxR6xpdVhqL8nI3ARQHl8BolAlgDbMOAHiNYlPsWzIjFjga+Et69zZs0nx3V5thfVSS+2FNgN69ZEa/XIY9mkkC0kAHmq/lLhvz+GXw/Bs21Y0JKY5RDCqaAi07Lln8HrdxCsHTyvcGXQ8ppME4J9KzXptY/Ppx86btuRw0MEce90eEkmP3ArFdxFoZNDx9EzLI0KiMfHMkKvskDQGMYskAJ8x0ISWffMrw7BvPgmKhmCwBlPo25uFkXm/7VamJoD2GLwbmlZ9Wn/y12E45qvmd/GxlMY/JNAdROTBEdreY+YTTCjRDj87OL8wtC3ZwkISQAi0rYMnEvzokKmFbwUdz56NdlZ2qnUTLNxFIHNOG/oixi6GLmlq0qvC8F5HGBmbANq9tHELwPkmTl3Ppm0p8VDlX9eGoQ1XzRb7MmVZdwO40c8WW24ysb2ZX5LirqncYo9IV5GboPiHBBobdDzu4HoNvNDc7CwbNtX+KOhoDmx6YFj/lMw5RDwfRCOCjqfnuJ5btnMb07vAS0mRANr7bJ823UjAkKDjcQe/xcyPhmEN/E3bVuMnWjMUaKHpM6+29mbNWj89NN/eH3Q8QTD3t9eJ9vu0iei7AEzprtOxkPUqqHnDHqtSrbuI6TYQsoKOp6fa9y44dvKT58PwbodfkjYBtHdgw/0DW8+aS4p6QdszrQYv+/dtzoagp7FnWp4rzAfR+ECD6T3j2pv1htl3Qg+cqRcQbj/re92GYea9YPrV6dMnnxo+Y2ng++VNa3l+TsyHNfh5k9qbdVefSwDtnakXMG4ypS13R8LWq+DQhgdz+2Vk3EyKFwKUG3Q8vdW2OmNSe7Ou6NMJoM2e5fNTB40fMlUBNxAw07TGGl8Sol4FJrY8PxdT25t1RBLAFyRZvaBeg19wmvjxIdMKA3+3vrrMvlQp68eGtTw/B67UzGv5NK3K+U5sd9DR9ITRn26vHXm9eGRaOm5MhnpBmHoVnGl5bmEhQKE/J7FTzLsG5cX+NugwekISQBclS72AwceY+ZmE1iuCXvv+XMtzg4uGzNgbzSsYE3QcPSEJoJv2P2OnZo20pipgLoiuJaAHh0gEL2y9Cg5vtHMz09U8QN1pUstzAGDwvuik2AVBx9ETkgB64dAme2BmJJIE9QKuZOZfNzc0Pj702ocCfa/exJbnzLw/mhf7m6Dj6AlTP7GhU7XJHpmaErkRxLcTkZH1grD1KjjT8hx0M8K8k5P58KC82PlBh9ETkgA88Fm9oPeHTgaFgd3QCEWvAgNanlcOmlRwXtBB9IQkAA8lQ72gdd17vcPOI4Mn2+8FGUtoz0lkVA3KKxgedBg9YXQCOFpmj7c0DSl/8oM3Z69bF+oNGYc22QP7RazZZGEuMyaYWC8IU6+C6lL7Qosid4FwKxEC7V7EzDXRvNjgIGPoKfM+he3UlBfdbJF6Fq2HSTgOr3t8u94e9LNrZ2resMeqFPWPIHUzAaODjqe7mHGCiUuaT/OyYdMLA+1VEIaW5wzURScVZAcxdm8ZnQBqS4vnKAur2/8zBh9k5heaHHp6+JTYrqBi66p258zdbNrhHcwMgEoBvTIMvQqCOieRGSeieQWD/BrPTWYngLKiOUqp1R3/Df6ImdcnGml1GA7oOJfP1QuA64xrv8VcpcFrmj5Vjw+/qiDQXgVHX31gSEq/TP9anht6NDhgegIoL7pVkXq6s7/X1vBBa/5t4mTjC0GvdXfG5HpBW4vuMPQq8LHl+alBkwqMOxkY6CMJoD1mTgC0SWv85mhd4uWLZ9uhbhB5ZEt8XJrF3wfRzQQyql7AjL1ghKJXQcvPEXcR0RwAA9y8NjMao3kFGW5e0y9GJ4C6sqLbSKlVPf3vW5a4UAro1WE/UKJk1iw1ad7fTbAsmgXD6gVh6lVQVx5/lIh+4uY1mTkRzYuluHlNv5idAMqL/olI/cqNazHjROt73r8N+xn1b5fcnT4mJ5pvYr2AwTvhYOWROmdtELOv2vKihxWpe928JjN0NK/AcvOafjE7AZTG7yCLVrp/Za5kwIhlxY9fWhTN6J85kyzMNWXvfKt6DX4hoZ3Hhk62P/Br0Lqt8cUEKnT7uoMmFRh5LxkZdJu6sqI7SCkPEsBnmHk/g0u4Wa/KmWaHuunDkVJ7XJpSxtULGNjJDpZV1SWe93opsbas+AGlsMTt62554n0r7JvRzsboBFBTXvQji9QK/0ZsWVYMex/5tnqBsugWBboRLhe9vNLWq6A5QSuGTY3t92KMuvL4PUT0S7evW1mdSAl6H0RPmJ0AyuJ3Wooe93vc9suKzY5+fthUO/BuvB0xsV7QvldBxTb9opt992rLi/63IvWYW9drs6u6NuNbsx8NtNNSTxidAGrLiu5USvmeANprW/dmjWerT9a/GHQTznM5sOmBYf1T028E1FwiBLJttrsYvA8aKxtPOb/Ovcbu9VuJXtWNDh460S/o9yN6IvTfBudECPxtMAIpEPLJQv7Q/v1X1pUXh3ZZ8avTH6oC8G8A/u1MvQBqTkhfsQUAEGg0FB5Oz4wkAPxrb6/HxI3kwfdeZk5W4J/FnjAy6DM4JK+DtiFKJ8LVRGpd9vghR+vK48/Wli3OL5k1K1xxAhieb++K5hX+vHTF+xckHH2lBj8J5tDOXpjYlccADeVJUk7VjUZ+mYbug9k9HHQAHSKigUR0s1LWlik//tqBuq3xZdWlRVcEHdcXzV63Tg/OL9yePSk2b1dN3WBmPYsZG5gRroJWS12g1xSxJ8/pkeaQfRl1kZFZqw2F4BGgSwgjCLQgYtGC4+XFuxi6RJ+m58LWS761iLUewPqDW+xh/ZSarRTdEI79BexKQtIaTcqDLTtWvzQzPotfYHQCAJMyroxJGEdQhVY6Cuu2xt9lxm9OOs4LI6fYVUGH1l5rPMsBLK/aVHRRaipuAGgOEY0KIh4ml2YAgCczgCZDW5obmbU+Y9rd/3kE+oYiejQrYn1cW1o8J+h4OjJseuFHLfWCisDqBcqlRwAN9qQGYOlmSQC+M+URoBMtKwk60LZWXdG+XvCXk46/9QIid2YAGt4kAEo3MgEYGfQZzAoGvSt/Ti5Ncf3SerzYegDrD214MDczI20mKTWXgMu8GI+1Oz8fB7pRefC9YRl6LxkZdBtN8KKeExBzE9n5Vy+pRFu9YLN9UWpE3QCiW13txkPuFAEdspq8eG83ITUA/3mxoSMw7M46d9CGTbVb6gVPVPzNZ/UC9Lpe4FoRkBxPioDEjpH3kpFBn8FsdvztcDIlM3yxXpDofb1AK1cSQFNjsyc1AGXobNrIoD/j8k3D3MCENcT0XRCGuXvxTri00y2Mzl4voLkE6nK9wK0ZgMUpnswAlFLGHfoCmD4DcHkVgAlN0Umxu7aseP+8hKOvZPByMPu0Pp9cM4COnH/1ksrsyYXLo5NiXz/dnLhYs/4FGJ3+jC3SrtQATlrerAIQayPvJSODPsPtR4DWdwvapq/RSbGFW1ZU+JIMlEtVbpMMm2p/lJ1XeF9bwj1XvYC1O8uA2FvrSQJwEDFyNm10AiBiVxcBCPylX6JvyUAl7yNAZ7pULyDtys9nzILHmloONHGXMnQVwMigz3B7DwCd+4WO2evWaaxbtx3A9pJZs+5u69JLjNkg6mXNoG88AnSmfb3g8EY7NyNNzSRSP3BrHwAAgNAElw9qPduXhwmMDPoMzQrKvRuHu/HzcD0ZJMkyoJtGzLDP7C/4sMR27bNKoEa4ngDMvJeMfgRwfxdgz7J4x48JnRe3zozMMgM4Fzf77TG7/z6Aw1oSgO9cXgUgkOptC/DPJ4P3u54M+nANwG+tMwCXrykzAP9p9zcCfdvFn0m3koFLb7uJzjG5vxRIhhYBjU4AXhz2eF601pNfZKfJIHk2NYYewf2uQARLEoDftAd3zamBaZ7/Itsng/e3Jc7T2pni6MR7Xo8rWjCT6zMAbegjgJFBn8FwvSNQVrq/mby1532gB2b2JdVl9qUAxrl9XakBBMGDR4CBOf3vdP2iIhT2bLSzLBX5LRHS3b+6mfsADE8A7sdPwJLassX5bl9XBC8nw1pJwFgvrk3KzCKOkUG3Ie1+K2YiKEXWs5Vb7BFuX1sEp7asaAFAN3l1fVNrAEYnAM96AhKGpVvWa7teuTfLk+sLX9WWx/OJ1CNejiE1gCCQdweDENGlQwYMeC6Mp/qIrjuyJT6OQOu8XqeXBBAEDx4B2iPg2sk//tqK3u4OFMGofM2Opll4jQied1zWHuwu9IPRCYBJe34aqyLcMf9K5fp58sJbO16z09P7Wa8Q0YVej8WMN4/WOL/2ehwvGJ0ATjXppQzs83ocpdQ9tWXFD3g9jnDHm7atRmdFniMiH85i5IPNDaducPNlJT8ZnQDOn26fSDTp6wF4PxNQWFJXFv+p1+OI3rFtG5dMjPyKgO96PRYzGh2Hvzf02oeOeT2WV4xOAAAwZFphhWa+y5fBCI/UlhWF9ggvASycaC0lwm1ej8PMgMbcnPzCHV6P5SXjEwAAZOfFnmHGE16PQ0QgUqtqSxd7/u0iuq+2PF4Aovv9GIuBWDS/oMSPsbyUFAkAAPbtObiQmT3fU0+ECFnWbyQJhEtdWfG9iijux1jMvPaxbU6xH2N5Lana0BzaZA/slxb5o1fbPdtjRkJD/yAnr3Ct12OJc6sri/+UFHm60acNM2+vP+hMHnWr7Ul3Yb8lVQIAgOpS+0LLivyRgKjXYzFDa/BdOXmx//B6LHF2tWVFC4homRe9Ib6Igd2NDYlv5V5j13k+mE+S5hGgzeB8e692cD17dA58e0RQClhRV158j9djiS+rLS++Xynly80PRlWzk5iWTDc/kIQJAABy8gu2waFb2Ic2Wy2FQfyytrzoYa/HEp+pKy9arAhLfRrulHYS/zA0397v03i+SbpHgPZqyuJ3Wooe92s8Bj9R+kTF/Nnr1kl/P4/Yto0FE61HiegnfozHYK0T+vqcKT9/1Y/x/JbUCQAAarfGH1Eg3zbwMOOpim2J21s7/QgX7Vh5R2T0mPNXEZEvezGYGazxw+z82FN+jBeEpHwEaK/siYqfAfy8X+MR4bZLJlqvyKvE7vqwxM68YOzIV/y6+QFAA4uS+eYH+sAMAGjZG37JRGsdEfm2ds/gisaEc1XuFPuwX2Mmq49fWhTNHJj5GkAT/BqTGcujeQUL/RovKEk/AwBaGm/+uabuHxko92tMAl2SYUXePrbZvsSvMZPR0VJ7VMbAzLf9vPm1xq+Xb0sk/c0P9JEZQJv319yTOfL8r2zx88MERoMD/n5OXmyDb2MmiaOlRd9MsegVAg3xa0xmfrlim/O9vlLD6VMJAGiZTmYMzNxKIN++mRmsmbEwOy/2736NabrqsuIbLcLT3nTwPTtm3lz7wbFrxix4LCl2+XVFn0sAAFC12c5Ji1hbQTTez3GZsbxiW+LuvvLt0hO2bWP+lVYhERb7ssGnDfP2yhpn2sWzbc9fLQ+TPpkAAODoqw8MSe2fuRXARX6Oy8wbjn3yyffH/cMvGvwc1wQ7XrPTL8iyVnnZvfesmN+pq2mYdsHsh+t9HTcE+mwCAFqTQFZGmd8zATDvatTO9cPz7V2+jhtiH7/x4IiMlIyXiHC5n+MyeOfJ087k86fbJ/wcNyz6dAIAgpsJAKjXzHOz82Iv+zxu6FSXFV9hKf5PP4t9AMDM733611OTz7t+aVLt7++OPrEMeC5Dr33oWP3pU5PB/IHPQw8g0H/WlRct7sutx2vL4gsswlb/b370+ZsfkBnAGZWv2dH0ftYbROTrFBQAwLzx05POLcn2prIs7+0AAAbtSURBVNm57NloZ0XTrVWKaLbfYzNQ0diQmNSXft4dkQTQzl9K7hsQzcl6Hb50k/0CxuGE1t8fnF+43fexfXZss31JJMVaRyDPG7d8CeOD04nEpGFT7Rrfxw6hPjv1PJsLZj9cf/DwX6cxsNn3wQkjLIt+n+yPBLWlxXNSUiJvB3HzM7CzsfGk3PztyAzgLPY/Y6cOGGmtI6JrgxifmUs/afr0lq9Of6gqiPG9cGDD/QOzMvutDGLKDwAM3lb7qXPVmBm2LL+2k7TfNL0x6la7qWKbc70GPxnE+ESU3z81879rSov9XQ/3yNGy4m/279fvT0Hd/GDetK/BmSY3/5fJDKATdWXF95JCYN1+mHn9ySbndhPXqVve3x8RA1EBwdtzHDvCzK/WH3RmJUsTT7dJAuiC2rKiO4nUY+TVceSdYPBBzZibkxd7M4jxe+JomT0+RUVWE3BZUDEw+KmK3zvSnOUcJAF0UW3Z4usUqd+AyLeXU9pjZgBY23jSWRjm5asdK++IjL5w5E+hOE6g1KDikPZsXSMJoBtqSosnKgsv+dFyvEPMVVrjruz82IuBxdCBUHzrt3SCXZSTF/vnoGIwiSSAbqr5XXysSqPXieD5sdPnwsyvftrceNd505YE3nHo/TX3ZI4YMeDnBPopEUWCioPBTY6muYMnF7wQVAymkQTQAx+/tCia8ZXM/ySibwccyinN+t+rP2mIB/V2YXVpfIal8DgRjQpi/DYM1DnN+vrBUwu3BRmHaSQB9NCe5fNTsy8eupIUbg06FgYfBPP/ieYVrvdrzGMb46Mj6XiEiK7za8yOMLBPN/J3cr4T2x10LKaRBNBLNeXx+xVoSVArBO0xeFuimRcNmVr4lldjtG7oeZAIC4Is8p3B/M7phHON7O7rGUkALqgpW3y1IutZIgwMOhYAAGOTTuifZ08tfNetS+5/xk7tf771IyKKESHHrev2BjO/uO+k84+XX2M3Bh2LqSQBuKTmd/GxVjq9BP/7CnSImTcwO4uzJ9s7enqNPcvnpw4aP/g2C/QgiEa4GV9PMTNAeKj0iYqYLPP1jiQAF+165d6sIf37r/bz/IGu4bdY87IjtfrFi2fbia78F62v696qCD8DaKTXEXYd1zsObsnJjyXlUV1+kwTgMtu2MX9i5H4iXhLU9teOcaVmrGhOYO2wqbH9Z/sbLcerW/MJdCuAAb6G1xnmD5zT+J4U+9wjCcAjteXxfCJ6jgBfO910RcsUmt6F5t82aqfEOd2sMzPSZyqFG5gxwdduvF3E4DVHqp0f97WuvV4L3286iRzcYg/LikSeIyAv6Fg60rLFmHQYVjE6UO9o/eOcyYW+ne/Yl4T1l54URk6xq5b/PjFZa72Qmbv07O03IkJYb35m7Eg089fl5veOzAB8Ur25aGIkhX4DUG7QsYRdS7Lkh47U6HhXi5aiZyQB+OjIxkU5aRn9VhEQSKchEzC4wtHO3MGT7feCjqUvkAQQgNryolsVqWUIW5U9QMycAPM/135YHe9LZ/MFTRJAQI68XjwyLYOfJqLQFgj9wsBOnUjcnjPF3hl0LH1NKIs/fcHwqwoOLt/mTGaH5wHcR5e2uF5rvbDi94m/l5s/GDIDCIGa38XHWmlYFch5BAFo6dnBaz9p+vS+ZOp8bCJJACFh2zbmXxGZQwqPhOVlGy8w8G6zxsKhkwveCToWIQkgdD5+aVE0fWDmUmLcEcYdeT3GfFhrevCx7Yk1tm0HHY1olUSfsOTSum9gBUChebuwRxgNDP2vf645vvRbsx+V13ZDRhJAiO1/xk7NGmn91CJaBMOWDJk5QUy/Pu0kYtKsI7wkARig8jU7mtZP3UekfkJA8F14zqG1wPeio51Fg/PtvUHHI85NEoBBWjoSYwkRzQw6li9qu/H1aTwor+uaQxKAgWrKFn/bIrUURN8MOhZmaCJ+wWlyFudMs+XGN4wkAIPVli3OJ6ViBJro99itbze+0NTES4dNL/zI7/GFOyQBJIFjW4onRCwsAvhqz5cOmRuY8NTpU/TI8KsKDno7mPCaJIAkUltmX04UuQ/g69w/oYcrmenR+vrEk6Ous+vdvbYIiiSAJHRwiz2sn2X9kyLc3tuGngy8qzUeO/7h0RJ5Sy/5SAJIYiWzZqnJPxqfR6TmAXQdEbo0K2BwExivJhL8qJeHjIjgSQLoIw5vtHMz0q3vEvA9ECaetWMx4wMNXtX411Nrzrt+aWiPIBfukQTQB1VttnNSI9Z1BHwPoEsZeFE7iVXySq4QQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCFE9/x/UcOIkMz9/D4AAAAASUVORK5CYII=",
        "company.name": "AusterFortia",
        "primary_color": "#298AAB",
        "secondary_color": "#7081e0",
        "font_name": "Roboto",
        "font_size": "16px",
        "font_url": "https://fonts.googleapis.com/css2?family=Roboto&display=swap",
        "global_margin": "6.35mm",
        "page_size": "A4",
        "page_layout": "portrait",
        "company_logo_size": "65%",
        "show_shipping_address_visibility": "0",
        "dir_text_align": "left",
        "show_paid_stamp": "none",
        "dir": "ltr",
        "status_logo": "",

    }

    ex_products = """
        <thead>
            <tr>
                <th data-ref="product_table-product.item-th" class="left-radius">Article</th>
                <th data-ref="product_table-product.description-th">Description</th>
                <th data-ref="product_table-product.unit_cost-th">Co&ucirc;t unitaire</th>
                <th data-ref="product_table-product.quantity-th">Quantit&eacute;</th>
                <th data-ref="product_table-product.discount-th" style="display: none">Remise</th>
                <th data-ref="product_table-product.line_total-th" class="right-radius">Total</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td data-ref="product_table-product.item-td" class="left-radius">Installation et cr&eacute;ation de
                    site WordPress</td>
                <td data-state="encoded-html" data-ref="product_table-product.description-td">
                    <p>Lancez votre pr&eacute;sence en ligne avec un site WordPress professionnel cr&eacute;&eacute;
                        sur mesure selon vos besoins.</p>
                    <p>Livrable :</p>
                    <ul>
                        <li>Un site WordPress enti&egrave;rement fonctionnel, responsive et optimis&eacute;,
                            pr&ecirc;t &agrave; accueillir vos visiteurs. Vous recevez tous les acc&egrave;s et une
                            documentation pour g&eacute;rer votre contenu en autonomie.</li>
                    </ul>
                    <p>D&eacute;lai de r&eacute;alisation : 5 &agrave; 10 jours ouvr&eacute;s</p>
                </td>
                <td style="white-space: nowrap" data-ref="product_table-product.unit_cost-td">120,00 &euro;</td>
                <td data-ref="product_table-product.quantity-td">1</td>
                <td data-ref="product_table-product.discount-td" style="display: none"></td>
                <td data-ref="product_table-product.line_total-td" class="right-radius">120,00 &euro;</td>
            </tr>
        </tbody>
    """

    ex_tasks = """
    <thead><tr><th data-ref="task_table-task.service-th" class="left-radius">Service</th><th data-ref="task_table-task.description-th">Description</th><th data-ref="task_table-task.hours-th">Heures</th><th data-ref="task_table-task.line_total-th" class="right-radius">Total</th></tr></thead><tbody><tr><td data-ref="task_table-task.service-td" class="left-radius">Installation et création de site WordPress</td><td data-state="encoded-html" data-ref="task_table-task.description-td"><p>Lancez votre présence en ligne avec un site WordPress professionnel créé sur mesure selon vos besoins.</p>
    <p>Livrable :</p>
    <ul>
    <li>Un site WordPress entièrement fonctionnel, responsive et optimisé, prêt à accueillir vos visiteurs. Vous recevez tous les accès et une documentation pour gérer votre contenu en autonomie.</li>
    </ul>
    <p>Délai de réalisation : 5 à 10 jours ouvrés</p>
    </td><td data-ref="task_table-task.hours-td">1</td><td data-ref="task_table-task.line_total-td" class="right-radius">120,00 €</td></tr></tbody>
    """

    ex_totals = """
    <div class="stamp is-paid"> Pay&eacute;</div>
            <div style="display: flex; flex-direction: column">
                <div data-ref="total_table-public_notes" style="text-align: left">
                    <div>&Agrave; payer apr&egrave;s finalisation de la cr&eacute;ation du site.</div>
                </div>
                <div style="text-align: left; display: flex; flex-direction: column; page-break-inside: auto">
                    <div data-ref="total_table-terms-label"
                        style="font-weight: bold; text-align: left; margin-top: 1rem; display: none">Conditions de
                        facturation: </div>
                    <div data-ref="total_table-terms" style="text-align: left"></div>
                </div><img style="max-width: 50%; height: auto" id="contact-signature">
                <div style="display: flex; align-items: flex-start; page-break-inside: auto"><img
                        src="https://invoicing.co/images/new_logo.png" style="height: 2.5rem; margin-top: 1.5rem"
                        id="invoiceninja-whitelabel-logo"></div>
            </div>
            <div class="totals-table-right-side" dir="ltr">
                <div class="totals_table-subtotal">
                    <p data-ref="totals_table-subtotal-label">Sous-total</p>
                    <p data-ref="totals_table-subtotal">120,00 &euro;</p>
                </div>
                <div class="totals_table-total">
                    <p data-ref="totals_table-total-label">Total</p>
                    <p data-ref="totals_table-total">120,00 &euro;</p>
                </div>
                <div class="totals_table-paid_to_date">
                    <p data-ref="totals_table-paid_to_date-label">Pay&eacute; &agrave; ce jour</p>
                    <p data-ref="totals_table-paid_to_date">0,00 &euro;</p>
                </div>
                <div class="totals_table-outstanding">
                    <p data-ref="totals_table-outstanding-label">Montant d&ucirc;</p>
                    <p data-ref="totals_table-outstanding">120,00 &euro;</p>
                </div>
            </div>
    """

    base = base.replace("<!--PRODUCTS-->", ex_products)
    base = base.replace("<!--TASKS-->", ex_tasks)
    base = base.replace("$status_logo", ex_totals)

    #<!--COMP-DETAILS-->
    #<!--COMP-ADRESS-->
    #<!--CLIENT-DET-->
    #<!--SHIP-DET-->
    #<!--ENTITY-DET-->

    base = base.replace("<!--COMP-DETAILS-->", """
        <p data-ref="company_details-company.name">AusterFortia</p>
        <p data-ref="company_details-company.id_number">915346431</p>
        <p data-ref="company_details-company.vat_number">FR54915346431</p>
        <p data-ref="company_details-company.website">austerfortia.fr</p>
        <p data-ref="company_details-company.email">charles-ivan@dury.dev</p>
    """)

    base = base.replace("<!--COMP-ADRESS-->", """
        <div data-ref="company_address-company.address1">33 RUE BAUDELAIRE</div>
        <div data-ref="company_address-company.city_state_postal">VOISINS LE BRETONNEUX 78960</div>
        <div data-ref="company_address-company.country">France</div>
    """)

    base = base.replace("<!--CLIENT-DET-->", """
    <div data-ref="client_details-client.name">RouleGalette</div>
                <div data-ref="client_details-client.address1">3 AVENUE DES CHEVALIERS TIREURS</div>
                <div data-ref="client_details-client.city_state_postal">CHAMBERY 73000</div>
                <div data-ref="client_details-client.country">France</div>
                <div data-ref="client_details-client.phone">0648614891</div>
                <div data-ref="client_details-contact.email">roulegalette73@gmail.com</div>
    """)

    base = base.replace("<!--SHIP-DET-->", """
    <div data-ref="shipping_address-label" style="font-weight: bold; text-transform: uppercase">Adresse de
                    Livraison</div>
                <div data-ref="shipping_address-client.city_state_postal"> </div>
    """)

    base = base.replace("<!--ENTITY-DET-->", """
    <tbody><tr>
            <th data-ref="entity_details-invoice.number_label">Numéro de facture</th>
            <th data-ref="entity_details-invoice.number">0010</th>
        </tr>
        <tr hidden="1">
            <th data-ref="entity_details-invoice.po_number_label">N° de Bon de Commande</th>
            <th data-ref="entity_details-invoice.po_number"> </th>
        </tr>
        <tr>
            <th data-ref="entity_details-invoice.date_label">Date de la facture</th>
            <th data-ref="entity_details-invoice.date">06-août-2025</th>
        </tr>
        <tr>
            <th data-ref="entity_details-invoice.due_date_label">Date limite</th>
            <th data-ref="entity_details-invoice.due_date">25-sept.-2025</th>
        </tr>
        <tr>
            <th data-ref="entity_details-invoice.total_label">Montant total</th>
            <th data-ref="entity_details-invoice.total">120,00 €</th>
        </tr>
        <tr>
            <th data-ref="entity_details-invoice.balance_due_label">Montant dû</th>
            <th data-ref="entity_details-invoice.balance_due">120,00 €</th>
        </tr>
        <tr hidden="1">
            <th data-ref="entity_details-invoice.project_label">Projet</th>
            <th data-ref="entity_details-invoice.project"></th>
        </tr>
    </tbody>
    """)

    for k,v in vars.items():
        base = base.replace(f"${k}", v)

    with open("preview.html", "w", encoding='utf-8') as f:
        f.write(base)





class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
    
    def on_modified(self, event):
        if not event.is_directory and os.path.abspath(event.src_path) == self.file_path:
            print(f"Le fichier {self.file_path} a été modifié !")
            self.action_personnalisee()
    
    def action_personnalisee(self):
        update()


chemin_fichier = "template.html"

event_handler = FileChangeHandler(chemin_fichier)
observer = Observer()

# Surveiller le dossier contenant le fichier
dossier = os.path.dirname(os.path.abspath(chemin_fichier))
observer.schedule(event_handler, dossier, recursive=False)

observer.start()
print(f"Surveillance du fichier : {chemin_fichier}")
print("Appuyez sur Ctrl+C pour arrêter...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    print("\nSurveillance arrêtée.")

observer.join()