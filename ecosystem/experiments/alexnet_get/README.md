> Superseded for new implementation work by [RFC 0.2 CPU reference](../alexneth_geot/README.md). This earlier planning artifact is preserved.

# Geometric Engine of Time × AlexNet Experimental (GET–AlexNet)

**Status: implementation proposal with a runnable planning scaffold.** No neural
network, trained weights, trainer, or accelerator backend is implemented here.

Start with [the complete framework](docs/IMPLEMENTATION_FRAMEWORK.md). It defines
the model, arithmetic boundaries, component ownership, data contracts, directory
layout, experimental controls, staged implementation instructions and release gates.

```sh
python3 ecosystem/experiments/alexnet_get/tools/plan.py validate
python3 ecosystem/experiments/alexnet_get/tools/plan.py list
python3 ecosystem/experiments/alexnet_get/tools/plan.py flow
```

These stdlib commands validate or describe the plan. They do not train a model.
`configs/experiments.v1.json` is the experimental matrix;
`contracts/scaffold.v1.json` lists **proposed** implementation files;
`contracts/flow.v1.json` is a neutral node/edge graph suitable for adapting to the
custom flowchart viewer. Its viewer-specific grammar was not available, so it is
not labeled a compatible import format without a real parser acceptance test.

The linked FractalOS conversation preview establishes an AlexNet-H investigation,
but its full text and 13 files are unavailable to this session. Earlier six-paper
research bundle and current repository code inform this new proposal. See
`docs/SOURCES_AND_DECISIONS.md` for provenance and unresolved decisions.
